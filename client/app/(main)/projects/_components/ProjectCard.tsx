"use client";

import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import Link from "next/link";
import type { Project } from "./types";

export default function ProjectCard({ project }: { project: Project }) {
  return (
    <Link href={`/projects/${project.id}`} className="block h-full">
      <motion.article
        whileHover={{ y: -5, scale: 1.02 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
        className="group relative flex h-full flex-col gap-5 rounded-3xl border border-white/5 bg-white/5 p-6 backdrop-blur-xl transition-colors hover:bg-white/10 hover:shadow-[0_24px_60px_-12px_rgba(124,92,224,0.15)] shadow-[0_24px_60px_-40px_rgba(11,15,20,0.7)]"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1.5">
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-foreground-3">
              {project.owner}
            </p>
            <div className="flex items-center gap-2">
              <h3 className="text-xl font-semibold text-foreground group-hover:text-observer-3 transition-colors">
                {project.name}
              </h3>
              <ArrowUpRight className="h-4 w-4 text-foreground-3 opacity-0 transition-all group-hover:opacity-100 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </div>
          </div>
        </div>
        
        <p className="text-sm leading-relaxed text-foreground-2/90 flex-grow">
          {project.description}
        </p>
        
        <div className="space-y-5">
          <div className="flex flex-wrap gap-2">
            {project.tags.map((tag) => (
              <span
                key={`${project.id}-${tag}`}
                className="rounded-full border border-white/5 bg-white/5 px-2.5 py-1 text-[11px] font-medium text-foreground-2 transition-colors group-hover:bg-white/10"
              >
                {tag}
              </span>
            ))}
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-medium">
              <span className="text-foreground-3">Progress</span>
              <span className="text-foreground-2">{project.progress}%</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/5">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${project.progress}%` }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
                className="h-full rounded-full bg-gradient-to-r from-observer to-observer-2 shadow-[0_0_10px_rgba(124,92,224,0.5)]"
              />
            </div>
          </div>
          
          <div className="flex items-center justify-between border-t border-white/5 pt-4">
             <p className="text-[11px] font-medium text-foreground-3">
              Updated {project.lastUpdate}
            </p>
            <div className="flex -space-x-2">
              {/* Placeholder for avatars if available in data later, strictly UI for now */}
            </div>
          </div>
        </div>
      </motion.article>
    </Link>

  );
}
