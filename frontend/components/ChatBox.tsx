"use client";

import { useState, useRef, useEffect } from "react";
import { Message } from "../types";
import { queryRepository } from "../services/api";
import { Send, User, Bot, Loader2 } from "lucide-react";
import { cn } from "../utils/cn";
import { RetrievedChunks } from "./RetrievedChunks";
import ReactMarkdown from "react-markdown";

interface ChatBoxProps {
  repoId: string;
}

export const ChatBox = ({ repoId }: ChatBoxProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I have ingested this repository. Ask me anything about its architecture, logic, or dependencies."
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { id: Date.now().toString(), role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await queryRepository(repoId, userMessage.content);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.answer,
        citations: response.citations
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [...prev, {
        id: Date.now().toString(),
        role: "assistant",
        content: "Sorry, I encountered an error while analyzing the repository. Please try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      
      {/* Header */}
      <div className="bg-slate-50 border-b border-slate-100 px-6 py-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-800">Intelligence Chat</h2>
        <div className="flex items-center space-x-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
          </span>
          <span className="text-xs font-medium text-slate-500 uppercase tracking-wide">Connected</span>
        </div>
      </div>

      {/* Message History */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50">
        {messages.map((msg) => (
          <div key={msg.id} className={cn("flex space-x-4 animate-in fade-in slide-in-from-bottom-2", msg.role === "user" ? "flex-row-reverse space-x-reverse" : "flex-row")}>
            <div className={cn("flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm", msg.role === "user" ? "bg-blue-600 text-white" : "bg-white border border-slate-200 text-slate-600")}>
              {msg.role === "user" ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>
            
            <div className={cn("max-w-[80%] rounded-2xl px-5 py-4", msg.role === "user" ? "bg-blue-600 text-white shadow-md rounded-tr-none" : "bg-white border border-slate-200 text-slate-800 shadow-sm rounded-tl-none")}>
              {msg.role === "user" ? (
                <div className="text-white whitespace-pre-wrap">{msg.content}</div>
              ) : (
                <div className="prose prose-sm max-w-none prose-p:leading-relaxed">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              )}
              {msg.citations && msg.citations.length > 0 && (
                <RetrievedChunks citations={msg.citations} />
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex space-x-4 animate-in fade-in">
             <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white border border-slate-200 text-slate-600 flex items-center justify-center">
              <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-none px-5 py-4 shadow-sm flex items-center space-x-2">
               <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce"></span>
               <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" style={{ animationDelay: "0.2s" }}></span>
               <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" style={{ animationDelay: "0.4s" }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-slate-100">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the codebase..."
            disabled={isLoading}
            className="w-full py-4 pl-4 pr-14 bg-slate-50 border border-slate-200 rounded-xl text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>

    </div>
  );
};
