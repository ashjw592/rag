const API_BASE = "/api";

/**
 * Send a chat message to the FastAPI backend.
 * The response is intentionally small to keep the UI fast and predictable.
 */
export async function sendChatMessage(message) {
  const response = await fetch(`${API_BASE}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed (${response.status})`);
  }

  return response.json();
}
