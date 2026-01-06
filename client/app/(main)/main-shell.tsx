"use client";

import Link from "next/link";
import { useState } from "react";
import { FolderKanban, LayoutGrid, Menu, PlusCircle, X } from "lucide-react";
import type { ReactNode } from "react";

export default function MainShell({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={`fixed left-6 top-6 z-40 rounded-full border border-observer/40 bg-background-2/80 p-2 text-foreground transition hover:text-foreground ${
          open ? "hidden" : "inline-flex"
        }`}
        aria-label="Abrir menu"
      >
        <Menu className="h-5 w-5" />
      </button>

      <aside
        className={`fixed left-0 top-0 z-40 flex h-screen w-64 flex-col gap-6 border-r border-observer/20 bg-background-2/80 p-6 shadow-[0_24px_60px_-40px_rgba(76,29,149,0.55)] transition-transform duration-300 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-foreground-3">
              IRAObserver
            </p>
            <p className="mt-2 text-lg font-semibold text-foreground">
              Dashboard
            </p>
          </div>
          <button
            type="button"
            onClick={() => setOpen(false)}
            className="rounded-full border border-observer/40 p-2 text-foreground transition hover:text-foreground-2"
            aria-label="Cerrar menu"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex flex-col gap-2 text-sm">
          <Link
            href="/room"
            className="flex items-center gap-3 rounded-xl border border-transparent px-3 py-2 text-foreground-2 transition hover:border-observer/40 hover:text-foreground"
          >
            <LayoutGrid className="h-4 w-4" />
            Room
          </Link>
          <Link
            href="/projects"
            className="flex items-center gap-3 rounded-xl border border-transparent px-3 py-2 text-foreground-2 transition hover:border-observer/40 hover:text-foreground"
          >
            <FolderKanban className="h-4 w-4" />
            Projects
          </Link>
          <Link
            href="/create-room"
            className="flex items-center gap-3 rounded-xl border border-transparent px-3 py-2 text-foreground-2 transition hover:border-observer/40 hover:text-foreground"
          >
            <PlusCircle className="h-4 w-4" />
            Create room
          </Link>
        </nav>

        <div className="mt-auto text-xs text-foreground-3">
          Status: connected
        </div>
      </aside>

      <div
        className={`min-h-screen transition-[padding] duration-300 ${
          open ? "pl-0 md:pl-72" : "pl-0"
        }`}
      >
        <div className="h-full w-full p-6">{children}</div>
      </div>
    </div>
  );
}
