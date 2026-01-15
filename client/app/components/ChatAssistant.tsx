"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Send, X, Bot, User, Loader2, Sparkles, SendHorizontal } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "./ui/card";
import { ScrollArea } from "./ui/scroll-area";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatAssistant() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hi! I'm Observer AI. How can I help with this project?",
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `I've analyzed your question. This feature is coming soon!`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="flex flex-col h-full max-h-full">
        <div className="flex-1 overflow-hidden">
            <ScrollArea className="h-full px-4 py-4">
                <div className="space-y-3">
                {messages.map((message) => (
                    <div
                    key={message.id}
                    className={cn(
                        "flex w-max max-w-[90%] flex-col gap-1 rounded-xl px-3 py-2 text-[11px] shadow-sm",
                        message.role === "assistant"
                        ? "bg-white/5 text-foreground-2 rounded-tl-none border border-white/5"
                        : "ml-auto bg-observer text-white rounded-tr-none shadow-observer/10"
                    )}
                    >
                        <div className="flex items-center gap-1.5 mb-0.5 opacity-70">
                            {message.role === "assistant" ? (
                            <Bot className="h-2.5 w-2.5 text-observer" />
                            ) : (
                            <User className="h-2.5 w-2.5 text-white/70" />
                            )}
                            <span className="text-[8px] font-bold uppercase tracking-tighter">
                            {message.role === "assistant" ? "Observer" : "You"}
                            </span>
                        </div>
                        <p className="leading-tight">{message.content}</p>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex w-max max-w-[90%] flex-col gap-1 rounded-xl rounded-tl-none bg-white/5 px-3 py-2 text-[11px] border border-white/5">
                        <div className="flex items-center gap-2">
                        <Loader2 className="h-2.5 w-2.5 animate-spin text-observer" />
                        <span className="text-[9px] font-bold uppercase tracking-tighter text-foreground-3 italic">
                            Analyzing...
                        </span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
                </div>
            </ScrollArea>
        </div>

        <div className="p-3 bg-black/20 border-t border-white/5">
            <form
                onSubmit={(e) => {
                e.preventDefault();
                handleSend();
                }}
                className="flex items-center gap-1.5"
            >
                <input
                    placeholder="Ask AI..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 bg-white/5 border border-white/5 rounded-lg px-2.5 py-1.5 text-[11px] text-foreground outline-none focus:border-observer/50 transition-colors"
                />
                <Button 
                    type="submit" 
                    size="icon" 
                    disabled={!input.trim() || isLoading}
                    className="h-7 w-7 bg-observer text-white hover:bg-observer/90"
                >
                    <SendHorizontal className="h-3 w-3" />
                </Button>
            </form>
        </div>
    </div>
  );
}
