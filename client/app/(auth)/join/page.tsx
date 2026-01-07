"use client";

import { motion } from "framer-motion";
import { ArrowRight, KeyRound } from "lucide-react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function JoinPage() {
  const router = useRouter();
  const [code, setCode] = useState("");

  const handleCodeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code.trim()) {
      router.push(`/register?code=${code}`);
    }
  };

  const handleCreate = () => {
    router.push("/register?action=create");
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <div className="mb-6 inline-flex items-center justify-center">
           <Image src="/ira-logo.png" alt="IRAObserver Logo" width={80} height={80} className="rounded-2xl" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-white">
          Welcome to <span className="text-observer">IRAObserver</span>
        </h1>
        <p className="mt-2 text-sm text-foreground-2">
          Join a session or manage your rooms
        </p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="space-y-6 rounded-3xl border border-white/5 bg-white/5 p-6 shadow-2xl shadow-black/50 backdrop-blur-2xl"
      >
        {/* Join by Code */}
        <div className="space-y-3">
          <label className="text-xs font-bold uppercase tracking-wider text-foreground-3">
            Join with code
          </label>
          <form onSubmit={handleCodeSubmit} className="flex gap-2">
            <div className="relative flex-1">
              <KeyRound className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-foreground-3" />
              <input
                type="text"
                placeholder="Enter room code..."
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-black/20 py-2.5 pl-10 pr-4 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:bg-black/40 focus:outline-none focus:ring-1 focus:ring-observer/50"
              />
            </div>
            <button
              type="submit"
              className="group flex aspect-square items-center justify-center rounded-xl bg-observer text-white transition hover:bg-observer-2 hover:shadow-[0_0_20px_rgba(124,92,224,0.4)] disabled:opacity-50"
              disabled={!code.trim()}
            >
              <ArrowRight className="h-4 w-4 transition-transform group-hover:-rotate-45" />
            </button>
          </form>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-white/5" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-[#10141d] px-2 text-foreground-3">or</span>
          </div>
        </div>

        {/* Create Room */}
        <button
          onClick={handleCreate}
          className="group flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-foreground transition hover:border-observer/40 hover:bg-observer/10 hover:text-white"
        >
          <span>Create a new room</span>
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/10 transition group-hover:bg-observer group-hover:text-white">
            <ArrowRight className="h-3 w-3" />
          </span>
        </button>

        <div className="relative">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-white/5" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-[#10141d] px-2 text-foreground-3">Login to account</span>
            </div>
        </div>

        {/* Login Form */}
        <form className="space-y-4">
            <div className="space-y-2">
                <input
                    type="text"
                    placeholder="Username"
                    className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-2.5 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:outline-none focus:ring-1 focus:ring-observer/50"
                />
                <input
                    type="password"
                    placeholder="Password"
                    className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-2.5 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:outline-none focus:ring-1 focus:ring-observer/50"
                />
            </div>
            <button
                type="button"
                className="w-full rounded-xl bg-white/10 py-2.5 text-sm font-semibold text-white transition hover:bg-white/20"
            >
                Log in
            </button>
        </form>
      </motion.div>
      
      <p className="text-center text-xs text-foreground-3">
        Don't have an account? <Link href="#" className="text-observer hover:underline hover:text-observer-2">Sign up</Link>
      </p>
    </div>
  );
}
