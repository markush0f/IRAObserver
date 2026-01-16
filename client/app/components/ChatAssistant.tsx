"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, X, Bot, User, Loader2, Sparkles, SendHorizontal } from "lucide-react";
import { Button } from "./ui/button";
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
  const [isOpen, setIsOpen] = useState(false);
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
        content: `I've analyzed your question. This feature is coming soon!`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="mb-4 w-80 sm:w-96"
          >
            <Card className="flex h-[450px] flex-col overflow-hidden border-observer/20 bg-background-2/95 shadow-2xl backdrop-blur-xl relative">
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => setIsOpen(false)}
                className="absolute top-3 right-3 z-20 h-7 w-7 text-foreground-3 hover:text-white"
              >
                <X className="h-4 w-4" />
              </Button>

              <CardContent className="flex-1 p-0 overflow-hidden pt-4">
                <ScrollArea className="h-full px-4 py-4">
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={cn(
                          "flex w-max max-w-[85%] flex-col gap-1 rounded-2xl px-4 py-2.5 text-xs shadow-sm",
                          message.role === "assistant"
                            ? "bg-white/5 text-foreground-2 rounded-tl-none border border-white/5"
                            : "ml-auto bg-observer text-white rounded-tr-none shadow-observer/10"
                        )}
                      >
                        <div className="flex items-center gap-1.5 mb-0.5 opacity-60">
                          {message.role === "assistant" ? (
                            <div className="h-3 w-3">
                                <img src="/ira-logo.png" alt="IRA" className="h-full w-full object-contain" />
                            </div>
                          ) : (
                            <User className="h-3 w-3" />
                          )}
                          <span className="text-[9px] font-bold uppercase tracking-tighter">
                            {message.role === "assistant" ? "Observer" : "You"}
                          </span>
                        </div>
                        <p className="leading-relaxed">{message.content}</p>
                      </div>
                    ))}
                    {isLoading && (
                      <div className="flex w-max max-w-[85%] flex-col gap-1 rounded-2xl rounded-tl-none bg-white/5 px-4 py-2.5 text-xs border border-white/5">
                        <div className="flex items-center gap-2">
                          <div className="h-3 w-3 animate-pulse">
                             <img src="/ira-logo.png" alt="IRA" className="h-full w-full object-contain" />
                          </div>
                          <span className="text-[9px] font-bold uppercase tracking-tighter text-foreground-3 italic">
                            Analyzing...
                          </span>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>
                </ScrollArea>
              </CardContent>

              <CardFooter className="border-t border-white/5 bg-black/20 p-3">
                <form onSubmit={handleSend} className="flex w-full items-center gap-2">
                  <input
                    placeholder="Ask a question..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 bg-white/5 border border-white/5 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-observer/50 transition-colors"
                  />
                  <Button 
                    type="submit" 
                    size="icon" 
                    disabled={!input.trim() || isLoading}
                    className="h-8 w-8 bg-observer text-white hover:bg-observer/90 shadow-lg shadow-observer/20 rounded-lg"
                  >
                    <SendHorizontal className="h-4 w-4" />
                  </Button>
                </form>
              </CardFooter>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          "flex h-14 w-14 items-center justify-center rounded-2xl shadow-2xl transition-all duration-300",
          isOpen 
            ? "bg-background-2 border border-white/10 text-white" 
            : "bg-observer text-white shadow-observer/20 ring-4 ring-observer/10"
        )}
      >
        {isOpen ? <X className="h-6 w-6" /> : <MessageSquare className="h-6 w-6" />}
      </motion.button>
    </div>
  );
}
