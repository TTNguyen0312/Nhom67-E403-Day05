from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from triage_tools import (
    check_emergency,
    detect_emergency_signals,
    format_emergency_response,
    lookup_specialty_info,
    suggest_specialties,
    triage_case,
)

load_dotenv('.env')

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / 'system_prompt.txt'
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding='utf-8')


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


TOOLS = [triage_case, check_emergency, suggest_specialties, lookup_specialty_info]
LLM = ChatOpenAI(model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'), temperature=0)
LLM_WITH_TOOLS = LLM.bind_tools(TOOLS)


def _preview_text(content, max_length: int = 180) -> str:
    # Rút gọn nội dung tool/message để log ra terminal cho dễ đọc.
    text = content if isinstance(content, str) else str(content)
    text = ' '.join(text.split())
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + '...'


def _latest_human_text(messages: list) -> str | None:
    # Lấy tin nhắn gần nhất của người dùng để phục vụ safety check và fallback.
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content if isinstance(message.content, str) else str(message.content)
    return None


def _human_turn_count(messages: list) -> int:
    # Đếm số lượt người dùng đã nói để hỗ trợ logic handoff trong fallback.
    return sum(1 for message in messages if isinstance(message, HumanMessage))


def _hard_safety_response(messages: list) -> AIMessage | None:
    # Chặn sớm các ca red flag trước khi gọi LLM để ưu tiên hướng dẫn đi cấp cứu.
    latest_human = _latest_human_text(messages)
    if not latest_human:
        return None

    signals = detect_emergency_signals(latest_human)
    if not signals:
        return None

    return AIMessage(content=format_emergency_response(signals))


def _fallback_response(user_text: str, turn_index: int = 1) -> str:
    # Fallback rule-based khi model/API lỗi để vẫn trả lời được các câu hỏi cơ bản.
    lowered = user_text.lower()

    if 'cấp cứu' in lowered or 'cap cuu' in lowered:
        return check_emergency.invoke({'symptoms': user_text})

    if any(phrase in lowered for phrase in ['khoa', 'chuyên khoa', 'chuyen khoa']) and any(
        token in lowered for token in ['khám gì', 'kham gi', 'là gì', 'la gi', 'vì sao', 'vi sao']
    ):
        specialty_hint = user_text
        for prefix in ['khoa ', 'chuyên khoa ', 'chuyen khoa ']:
            if prefix in lowered:
                start = lowered.index(prefix) + len(prefix)
                specialty_hint = user_text[start:].strip(' ?')
                break
        return lookup_specialty_info.invoke({'specialty': specialty_hint})

    if any(
        phrase in lowered
        for phrase in ['không đúng', 'khong dung', 'không phải', 'khong phai', 'chưa đúng', 'chua dung']
    ):
        return triage_case.invoke(
            {
                'symptoms': user_text,
                'previous_feedback': user_text,
                'turn_index': turn_index,
            }
        )

    if user_text.strip():
        return triage_case.invoke({'symptoms': user_text, 'turn_index': turn_index})

    return (
        'Mình đang gặp sự cố kết nối với mô hình ngôn ngữ nên chỉ hỗ trợ được mức cơ bản lúc này. '
        'Bạn có thể mô tả triệu chứng hoặc hỏi trực tiếp kiểu như “nên khám khoa nào?” để mình định hướng sơ bộ.'
    )


def agent_node(state: AgentState) -> AgentState:
    # Node chính của graph: chèn system prompt, chạy safety check, rồi gọi model/tool.
    messages = state['messages']

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    safety_message = _hard_safety_response(messages)
    if safety_message is not None:
        print('[Safety] Emergency red flag detected')
        return {'messages': [safety_message]}

    try:
        response = LLM_WITH_TOOLS.invoke(messages)
    except Exception as exc:
        print(f'[Agent error] {type(exc).__name__}: {exc}')
        latest_human = _latest_human_text(messages) or ''
        response = AIMessage(
            content=_fallback_response(
                latest_human, turn_index=max(1, _human_turn_count(messages))
            )
        )

    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"[Tool call] {tool_call['name']}({tool_call['args']})")
    else:
        print('[Agent] Trả lời trực tiếp')

    return {'messages': [response]}


def build_graph():
    # Tạo luồng agent -> tools -> agent để model có thể gọi tool nhiều bước nếu cần.
    builder = StateGraph(AgentState)
    builder.add_node('agent', agent_node)
    builder.add_node('tools', ToolNode(TOOLS))

    builder.add_edge(START, 'agent')
    builder.add_conditional_edges('agent', tools_condition)
    builder.add_edge('tools', 'agent')

    return builder.compile()


GRAPH = build_graph()


def run_turn(user_input: str, history: list | None = None):
    # Chạy một lượt hội thoại với lịch sử hiện có và trả về toàn bộ message mới nhất.
    current_history = history or []
    input_messages = current_history + [HumanMessage(content=user_input)]
    result = GRAPH.invoke({'messages': input_messages})
    messages = result['messages']
    all_messages = messages if isinstance(messages, list) else [messages]

    new_messages = all_messages[len(current_history) + 1 :]
    for message in new_messages:
        if isinstance(message, ToolMessage):
            print(f'[Tool result] {_preview_text(message.content)}')

    return all_messages


def main() -> None:
    # CLI đơn giản để chat thử agent ngay trong terminal.
    print('=' * 60)
    print('Vinmec Triage Assistant - Trợ lý định hướng chuyên khoa')
    print("Gõ 'quit' để thoát")
    print('=' * 60)

    history: list = []

    while True:
        user_input = input('\nBạn: ').strip()
        if user_input.lower() in {'quit', 'exit', 'q'}:
            break

        print('\n[Vinmec Triage Assistant đang suy nghĩ...]')
        history = run_turn(user_input, history)
        final_message = history[-1]
        print(f'\nVinmec Triage Assistant: {final_message.content}')


if __name__ == '__main__':
    main()
