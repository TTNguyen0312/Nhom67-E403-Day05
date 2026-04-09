from __future__ import annotations

from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools import calculate_budget, search_flights, search_hotels


load_dotenv(".env")

# Đọc SYSTEM PROMPT
SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "system_prompt.txt"
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

# Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Khởi tạo LLM và tools
TOOLS = [search_flights, search_hotels, calculate_budget]
LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
LLM_WITH_TOOLS = LLM.bind_tools(TOOLS)


def _preview_text(content, max_length: int = 180) -> str:
    text = content if isinstance(content, str) else str(content)
    text = " ".join(text.split())
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


# Agent node
def agent_node(state: AgentState) -> AgentState:
    messages = state["messages"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    try:
        response = LLM_WITH_TOOLS.invoke(messages)
    except Exception as exc:
        print(f"[Agent error] {type(exc).__name__}: {exc}")
        response = AIMessage(
            content=(
                "Xin lỗi, hệ thống đang gặp sự cố khi xử lý yêu cầu của bạn. "
                "Bạn hãy thử lại sau ít phút nhé."
            )
        )

    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"[Tool call] {tool_call['name']}({tool_call['args']})")
    else:
        print("[Agent] Trả lời trực tiếp")

    return {"messages": [response]}

# Xây dựng graph
def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    tool_node = ToolNode(TOOLS)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


GRAPH = build_graph()


def run_turn(user_input: str, history: list | None = None):
    current_history = history or []
    input_messages = current_history + [HumanMessage(content=user_input)]
    result = GRAPH.invoke({"messages": input_messages})
    messages = result["messages"]
    all_messages = messages if isinstance(messages, list) else [messages]

    new_messages = all_messages[len(current_history) + 1 :]
    for message in new_messages:
        if isinstance(message, ToolMessage):
            print(f"[Tool result] {_preview_text(message.content)}")

    return all_messages

def main() -> None:
    print("=" * 60)
    print("TravelBuddy - Trợ lý du lịch thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    history: list = []

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            break

        print("\n[TravelBuddy đang suy nghĩ...]")
        history = run_turn(user_input, history)
        final_message = history[-1]
        print(f"\nTravelBuddy: {final_message.content}")


if __name__ == "__main__":
    main()
