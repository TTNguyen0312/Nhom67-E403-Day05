const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendMessageToAgent(payload) {
  const response = await fetch(`${API_BASE_URL}/api/agent/triage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }

  return response.json();
}