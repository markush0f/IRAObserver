"use client";

import { motion } from "framer-motion";
import { ArrowRight, Check } from "lucide-react";
import Image from "next/image";
import { useSearchParams, useRouter } from "next/navigation";
import { Suspense } from "react";

function RegisterContent() {
  const params = useSearchParams();
  const router = useRouter();
  const code = params.get("code");
  const action = params.get("action");

  const titleText = action === "create" ? "Set up your profile" : "Join Session";
  const subText =
    action === "create"
      ? "Create an account to start your new room."
      : code
      ? `Register to join room #${code}`
      : "Create an account to continue.";

  return (
    <div className="space-y-8">
      <div className="text-center">
        <div className="mb-6 inline-flex items-center justify-center">
           <Image src="/ira-logo.png" alt="IRAObserver Logo" width={80} height={80} className="rounded-2xl" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-white">
          {titleText}
        </h1>
        <p className="mt-2 text-sm text-foreground-2">{subText}</p>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="rounded-3xl border border-white/5 bg-white/5 p-8 shadow-2xl shadow-black/50 backdrop-blur-2xl"
      >
        <form className="space-y-5" onSubmit={(e) => { e.preventDefault(); router.push('/projects'); }}>
          <div className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold uppercase tracking-wider text-foreground-3 ml-1">
                Username
              </label>
              <input
                type="text"
                required
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:bg-black/40 focus:outline-none focus:ring-1 focus:ring-observer/50"
                placeholder="Choose a username"
              />
            </div>
            
            <div className="space-y-1.5">
              <label className="text-xs font-semibold uppercase tracking-wider text-foreground-3 ml-1">
                Password
              </label>
              <input
                type="password"
                required
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:bg-black/40 focus:outline-none focus:ring-1 focus:ring-observer/50"
                placeholder="Create a password"
              />
            </div>

            <div className="space-y-1.5">
               <label className="text-xs font-semibold uppercase tracking-wider text-foreground-3 ml-1">
                Confirm Password
              </label>
              <input
                type="password"
                required
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-foreground placeholder:text-foreground-3/50 focus:border-observer/50 focus:bg-black/40 focus:outline-none focus:ring-1 focus:ring-observer/50"
                placeholder="Confirm your password"
              />
            </div>
          </div>

          <button
            type="submit"
            className="group mt-2 flex w-full items-center justify-center gap-2 rounded-xl bg-observer py-3.5 text-sm font-semibold text-white shadow-[0_0_20px_rgba(124,92,224,0.3)] transition-all hover:bg-observer-2 hover:shadow-[0_0_30px_rgba(124,92,224,0.5)]"
          >
            <span>Complete Registration</span>
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </button>
        </form>
      </motion.div>

      <div className="flex justify-center gap-6 text-xs text-foreground-3">
         <span className="flex items-center gap-1.5">
            <Check className="h-3.5 w-3.5 text-success" /> Free forever
         </span>
          <span className="flex items-center gap-1.5">
            <Check className="h-3.5 w-3.5 text-success" /> No credit card
         </span>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense fallback={<div className="text-foreground-3 text-sm">Loading...</div>}>
      <RegisterContent />
    </Suspense>
  );
}
