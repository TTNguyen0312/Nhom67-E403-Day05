import { useState, useEffect, useRef } from 'react';
import { Shell, Bubble, TypingDots } from '../components';
import { colors } from '../styles/tokens';
import { sendMessageToAgent } from "../services/agentApi";

export default function TriageScreen({ onEmergency, onSuggest, onEscalate, goHome }) {
  const [msgs, setMsgs] = useState([
    {
      id: 0,
      ai: true,
      text: 'Xin chào! Tôi là trợ lý AI sàng lọc triệu chứng.\n\nBạn đang gặp triệu chứng gì?',
    },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const scrollRef = useRef(null);

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

  const send = async () => {
    const txt = input.trim();
    if (!txt || typing) return;

    addUserMsg(txt);
    setInput('');
    setTyping(true);

    try {
      const data = await sendMessageToAgent({
        message: txt,
        session_id: "session-001",
      });

      setTyping(false);

      addAIMsg(data.reply || "Không có phản hồi từ hệ thống.");

      if (data.next_screen === "EmergencyScreen") {
        setTimeout(() => onEmergency?.(data), 800);
      } else if (data.next_screen === "SpecialtyScreen") {
        setTimeout(() => onSuggest?.(data), 800);
      } else if (data.next_screen === "EscalateScreen") {
        setTimeout(() => onEscalate?.(data), 800);
      }
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
            <span style={{ whiteSpace: 'pre-line' }}>{m.text}</span>
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