"use client";

import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { motion } from "framer-motion";
import { useState, useRef, useEffect } from "react";
import { 
  SendHorizontal, 
  Loader2, 
  Terminal,
  Cpu,
  ShieldAlert,
  Zap,
  User
} from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { ScrollArea } from "@/app/components/ui/scroll-area";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function AssistantPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject } = useProject(projectId);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I am the Observer AI Assistant. How can I help you today?",
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

  if (loadingProject) {
    return <div className="flex h-[calc(100vh-48px)] items-center justify-center text-foreground-3">Initializing AI Agent...</div>;
  }

  if (!project) {
    notFound();
    return null;
  }

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
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
        content: `I've analyzed your question about "${input}". This feature is currently in simulation mode.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="fixed inset-0 lg:left-64 bg-background z-10 flex flex-col">
      {/* Main Chat Area */}
      <div className="flex-1 min-h-0 flex flex-col relative bg-background font-sans">
        <ScrollArea className="flex-1 p-6 md:p-10">
          <div className="max-w-4xl mx-auto space-y-8 pb-10 pt-4">
            {messages.map((message) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={message.id}
                className={cn(
                  "flex w-full gap-5",
                  message.role === "user" ? "flex-row-reverse" : "flex-row"
                )}
              >
                <div className={cn(
                    "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border p-1.5 transition-colors",
                    message.role === "assistant" 
                        ? "bg-white/5 border-white/10" 
                        : "bg-white/10 border-white/10 text-white"
                )}>
                  {message.role === "assistant" ? <img src="/ira-logo.png" alt="IRA" className="h-full w-full object-contain" /> : <User className="h-6 w-6" />}
                </div>

                <div className={cn(
                  "flex flex-col gap-2 max-w-[85%]",
                  message.role === "user" ? "items-end" : "items-start"
                )}>
                  <div className={cn(
                    "rounded-2xl px-6 py-4 text-[15px] shadow-sm leading-relaxed",
                    message.role === "assistant"
                      ? "bg-white/5 text-foreground-2 border border-white/5"
                      : "bg-observer text-white shadow-lg shadow-observer/20"
                  )}>
                    {message.content}
                  </div>
                  <span className="text-[10px] text-foreground-3 opacity-40 px-1 font-mono">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </motion.div>
            ))}
            {isLoading && (
              <div className="flex w-full gap-5">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 border border-white/10 p-2">
                  <div className="h-full w-full animate-pulse">
                    <img src="/ira-logo.png" alt="IRA" className="h-full w-full object-contain" />
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <div className="bg-white/5 border border-white/5 rounded-2xl px-6 py-4 flex items-center gap-3">
                    <Loader2 className="h-4 w-4 animate-spin text-observer" />
                    <span className="text-sm text-foreground-3 italic">Analyzing repository...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Form Area */}
        <div className="p-6 md:p-10 bg-background border-t border-white/5">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSend} className="relative group">
              <input
                type="text"
                placeholder="Message Observer AI..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-white/5 py-4 pl-6 pr-16 text-base text-white placeholder:text-foreground-3 outline-none focus:border-observer/50 focus:bg-white/[0.07] transition-all"
              />
              <Button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 h-11 w-11 bg-observer text-white hover:bg-observer/90 rounded-xl transition-transform active:scale-95"
                size="icon"
              >
                <SendHorizontal className="h-5 w-5" />
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
