"use client";

import { useEffect, useRef, useState } from "react";
import api from "@/lib/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; 


export function Chat({ notebookId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await api.get(
          `/notebooks/${notebookId}/chat/`
        );

        setMessages(response.data);
      } catch (error) {
        console.error("Failed to load messages:", error);
      }
    };

    loadMessages();
  }, [notebookId]);

  // Auto-scroll to the latest message whenever the list changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    const query = input.trim();

    if (!query || sending) return;

    const userMessage = {
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setSending(true);

    try {
      const response = await api.post(
        `/notebooks/${notebookId}/chat/`,
        {
          query,
        }
      );

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Scrollable messages area */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-6 pr-2">
        {messages.map(({ role, content }, index) => {
          const isUser = role === "user";

          if (isUser) {
            return (
              <div key={index} className="flex justify-end">
                <div className="bg-teal text-cream px-4 py-3 rounded-lg max-w-[80%] font-ui text-sm">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                </div>
              </div>
            );
          }

          return (
            <div
              key={index}
              className="flex flex-col items-start max-w-[85%]"
            >
              <p className="text-xs font-ui tracking-wide text-teal mb-1">
                TUTOR
              </p>

              <div className="text-oxblood font-display">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
              </div>
            </div>
          );
        })}

        {/* Typing indicator - shows while sending */}
        {sending && (
          <div className="flex flex-col items-start max-w-[85%]">
            <p className="text-xs font-ui tracking-wide text-teal mb-1">
              TUTOR
            </p>
            <div className="flex gap-1 bg-cream px-4 py-3 rounded-lg">
              <span className="w-2 h-2 rounded-full bg-teal animate-bounce [animation-delay:0ms]" />
              <span className="w-2 h-2 rounded-full bg-teal animate-bounce [animation-delay:150ms]" />
              <span className="w-2 h-2 rounded-full bg-teal animate-bounce [animation-delay:300ms]" />
            </div>
          </div>
        )}

        {/* Scroll anchor - always stays at the bottom of the list */}
        <div ref={bottomRef} />
      </div>

      {/* Fixed input area - stays at bottom */}
      <div className="flex gap-3 pt-4 shrink-0">
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              sendMessage();
            }
          }}
          placeholder="Ask a question..."
          rows={1}
          className="flex-1 min-w-0 rounded-lg border border-teal px-3 py-2 text-sm resize-none"
          disabled={sending}
        />

        <button
          type="button"
          onClick={sendMessage}
          disabled={sending || !input.trim()}
          className="bg-teal text-cream px-4 py-2 rounded-lg font-ui text-sm disabled:opacity-50"
        >
          {sending ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default function ChatPanel({ notebookId }) {
  return <Chat notebookId={notebookId} />;
}
