import { useState, useEffect, useRef } from 'react';
import { Shell, Bubble, TypingDots } from '../components';
import { colors } from '../styles/tokens';
import { EMERGENCY_KEYWORDS, AI_QUESTIONS } from '../data/constants';
import { sendMessageToAgent } from "../services/agentApi";

function renderText(text) {
  if (!text) return null;
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <span style={{ whiteSpace: 'pre-line' }}>
      {parts.map((part, i) =>
        part.startsWith('**') && part.endsWith('**')
          ? <strong key={i}>{part.slice(2, -2)}</strong>
          : part
      )}
    </span>
  );
}
export default function TriageScreen({ onEmergency, onSuggest, onEscalate, goHome }) {
  const [msgs, setMsgs] = useState([
    {
      id: 0,
      ai: true,
      text: 'Xin chào! Tôi là trợ lý AI sàng lọc triệu chứng.\n\nBạn đang gặp triệu chứng gì?',
    },
  ]);
  const [input, setInput] = useState('');
  const [round, setRound] = useState(0);
  const [entered, setEntered] = useState(false);
  const [typing, setTyping] = useState(false);
  const [sessionId, setSessionId] = useState(
    () => new URLSearchParams(window.location.search).get('session_id')
  );
  const scrollRef = useRef(null);

  /* Auto-scroll on new messages */
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [msgs, typing]);

  const addAIMsg = (text) => {
    setMsgs((p) => [...p, { id: Date.now() + 1, ai: true, text }]);
  };

  const addUserMsg = (text) => {
    setMsgs((p) => [...p, { id: Date.now(), ai: false, text }]);
  };

  // const send = () => {
  //   const txt = input.trim();
  //   if (!txt || typing) return;

  //   setMsgs((p) => [...p, { id: Date.now(), ai: false, text: txt }]);
  //   setInput('');

  //   /* ── Emergency check ── */
  //   if (EMERGENCY_KEYWORDS.some((kw) => txt.toLowerCase().includes(kw))) {
  //     setTyping(true);
  //     setTimeout(() => {
  //       setTyping(false);
  //       onEmergency();
  //     }, 1200);
  //     return;
  //   }

  //   setTyping(true);

  //   /* ── First symptom entry ── */
  //   if (!entered) {
  //     setEntered(true);
  //     setTimeout(() => {
  //       setTyping(false);
  //       addAIMsg(`Cảm ơn bạn. Để đánh giá chính xác hơn:\n\n${AI_QUESTIONS[0]}`);
  //       setRound(1);
  //     }, 1400);
  //     return;
  //   }

  //   /* ── Follow-up rounds ── */
  //   const next = round + 1;
  //   setTimeout(() => {
  //     setTyping(false);
  //     if (next < 3) {
  //       addAIMsg(AI_QUESTIONS[next] || 'Bạn có thêm thông tin nào khác?');
  //       setRound(next);
  //     } else if (next === 3) {
  //       addAIMsg('Cảm ơn bạn. Dựa trên mô tả, tôi sẽ gợi ý chuyên khoa phù hợp.');
  //       setTimeout(onSuggest, 900);
  //     } else {
  //       /* Over 3 rounds → escalate */
  //       onEscalate();
  //     }
  //   }, 1400);


  // };
  const send = async () => {
  const txt = input.trim();
  if (!txt || typing) return;

  addUserMsg(txt);
  setInput('');
  setTyping(true);

  try {
    const data = await sendMessageToAgent({
      message: txt,
      session_id: sessionId,
    });

    if (data.session_id) {
      setSessionId(data.session_id);
      const params = new URLSearchParams(window.location.search);
      params.set('session_id', data.session_id);
      window.history.replaceState(null, '', `?${params.toString()}`);
    }
    setTyping(false);
    addAIMsg(data.reply || "Không có phản hồi từ hệ thống.");
  } catch (error) {
    setTyping(false);
    addAIMsg("Xin lỗi, hiện tại chưa thể kết nối tới hệ thống.");
    console.error(error);
  }
};
  return (
    <Shell
      title="Sàng lọc triệu chứng"
      subtitle="AI Triage"
      onBack={goHome}
      footer={
        <div style={{ display: 'flex', gap: 10 }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
            placeholder="Mô tả triệu chứng..."
            style={{
              flex: 1,
              border: `2px solid ${colors.g200}`,
              borderRadius: 14,
              padding: '12px 16px',
              fontSize: 15,
              background: colors.g100,
              transition: 'border-color 0.2s',
            }}
            onFocus={(e) => (e.target.style.borderColor = colors.teal)}
            onBlur={(e) => (e.target.style.borderColor = colors.g200)}
          />
          <button
            onClick={send}
            aria-label="Gửi"
            style={{
              width: 46,
              height: 46,
              borderRadius: 14,
              border: 'none',
              flexShrink: 0,
              background: `linear-gradient(135deg, ${colors.teal}, ${colors.tealDark})`,
              color: colors.white,
              fontSize: 20,
              boxShadow: '0 4px 12px rgba(0,137,123,0.3)',
            }}
          >
            ↑
          </button>
        </div>
      }
    >
      <div
        ref={scrollRef}
        style={{ flex: 1, overflowY: 'auto', padding: '20px 0' }}
      >
        {msgs.map((m) => (
          <Bubble key={m.id} isAI={m.ai}>
            {renderText(m.text)}
          </Bubble>
        ))}
        {typing && (
          <Bubble isAI>
            <TypingDots />
          </Bubble>
        )}
      </div>
    </Shell>
  );
}
