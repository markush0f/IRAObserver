"use client";

import Link from "next/link";
import { useState } from "react";
import { 
  Menu, 
  X, 
  LayoutDashboard, 
  Settings, 
  Activity, 
  ArrowLeft,
  KanbanSquare,
  GitBranch as GitBranchIcon,
  PieChart,
  Layers,
  Globe,
  Sparkles
} from "lucide-react";
import type { ReactNode } from "react";
import { useParams, usePathname } from "next/navigation";
import { useProject } from "@/hooks/useProject";

export default function ProjectShell({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(true);
  const params = useParams();
  const pathname = usePathname();
  const projectId = params.projectId as string;
  
  const { project } = useProject(projectId);
  
  const isActive = (path: string) => pathname === path;
  
  const baseUrl = `/projects/${projectId}`;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={`fixed left-6 top-6 z-40 rounded-full border border-observer/40 bg-background-2/80 p-2 text-foreground transition hover:text-foreground ${
          open ? "hidden" : "inline-flex"
        }`}
        aria-label="Open menu"
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
            <Link 
              href="/projects" 
              className="group mb-2 flex items-center gap-2 text-xs font-medium text-foreground-3 transition-colors hover:text-foreground"
            >
              <ArrowLeft className="h-3 w-3 transition-transform group-hover:-translate-x-1" />
              ALL PROJECTS
            </Link>
            <p className="mt-1 truncate text-lg font-semibold text-foreground" title={project?.name || "Project"}>
              {project?.name || "Project"}
            </p>
          </div>
          <button
            type="button"
            onClick={() => setOpen(false)}
            className="rounded-full border border-observer/40 p-2 text-foreground transition hover:text-foreground-2"
            aria-label="Close menu"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex flex-col gap-2 text-sm">
          <Link
            href={baseUrl}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(baseUrl) 
                ? "border-observer bg-observer/10 text-white" 
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <LayoutDashboard className="h-4 w-4" />
            Overview
          </Link>
          <Link
            href={`${baseUrl}/board`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/board`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <KanbanSquare className="h-4 w-4" />
            Board
          </Link>
           <Link
            href={`${baseUrl}/activity`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/activity`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <Activity className="h-4 w-4" />
            Activity
          </Link>
          <Link
            href={`${baseUrl}/git`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/git`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <GitBranchIcon className="h-4 w-4" />
            Git
          </Link>
          <Link
            href={`${baseUrl}/technologies`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/technologies`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <Layers className="h-4 w-4" />
            Technologies
          </Link>
          <Link
            href={`${baseUrl}/endpoints`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/endpoints`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <Globe className="h-4 w-4" />
            Endpoints
          </Link>
          <Link
            href={`${baseUrl}/assistant`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/assistant`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <Sparkles className="h-4 w-4" />
            AI Assistant
          </Link>
          <div className="my-2 border-t border-white/5" />
          <Link
            href={`${baseUrl}/analysis`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/analysis`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <PieChart className="h-4 w-4" />
            Analysis
          </Link>
          <Link
            href={`${baseUrl}/settings`}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 transition ${
              isActive(`${baseUrl}/settings`)
                ? "border-observer bg-observer/10 text-white"
                : "border-transparent text-foreground-2 hover:border-observer/40 hover:text-foreground"
            }`}
          >
            <Settings className="h-4 w-4" />
            Settings
          </Link>
        </nav>

        <div className="mt-auto flex flex-col gap-4 overflow-hidden">
             <div className="rounded-xl border border-white/5 bg-white/5 p-4">
                <p className="mb-2 text-xs font-semibold text-foreground-3">Analysis Status</p>
                <div className="flex items-center gap-2">
                    <span className={`flex h-2 w-2 rounded-full ${project?.last_analysis_at ? 'bg-green-500' : 'bg-yellow-500'}`} />
                    <span className="text-sm font-medium capitalize text-foreground">{project?.last_analysis_at ? 'Analyzed' : 'Pending'}</span>
                </div>
            </div>
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
