// React is loaded via ESM so the UI works without a build step.
import React from "https://esm.sh/react@18";
import { createRoot } from "https://esm.sh/react-dom@18/client";

import { sendChatMessage } from "./api.js";

const { useState } = React;
const h = React.createElement;

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");

  const statusText = isSending ? "Thinking..." : "Ready";

  async function handleSubmit(event) {
    event.preventDefault();
    const trimmed = input.trim();

    if (!trimmed || isSending) {
      return;
    }

    setIsSending(true);
    setError("");
    setInput("");

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);

    try {
      const response = await sendChatMessage(trimmed);
      setMessages((prev) => [...prev, { role: "assistant", content: response.reply }]);
    } catch (err) {
      setError(err?.message ?? "Something went wrong.");
    } finally {
      setIsSending(false);
    }
  }

  const transcript =
    messages.length === 0
      ? h("div", { className: "empty" }, "No messages yet. Ask a question to begin.")
      : messages.map((message, index) =>
          h(
            "div",
            {
              key: `${message.role}-${index}`,
              className: `message message--${message.role}`,
            },
            message.content
          )
        );

  return h(
    "div",
    { className: "shell" },
    h(
      "header",
      { className: "header" },
      h("h1", null, "RAG Chat"),
      h("p", null, "Ask questions about the PDFs you ingest into the vector store.")
    ),
    h("section", { className: "chat", "aria-live": "polite" }, transcript),
    h(
      "form",
      { className: "composer", onSubmit: handleSubmit },
      h("input", {
        type: "text",
        name: "message",
        placeholder: "Type a question...",
        value: input,
        onChange: (event) => setInput(event.target.value),
        disabled: isSending,
        autoComplete: "off",
      }),
      h(
        "button",
        { type: "submit", disabled: isSending || !input.trim() },
        isSending ? "Sending..." : "Send"
      )
    ),
    h(
      "footer",
      { className: "status" },
      h("span", null, h("strong", null, "Status:"), ` ${statusText}`),
      error ? h("span", { className: "error" }, error) : null
    )
  );
}

const root = createRoot(document.getElementById("app"));
root.render(h(App));
