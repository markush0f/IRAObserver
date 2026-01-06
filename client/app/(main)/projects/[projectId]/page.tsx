"use client";

import Link from "next/link";
import { ArrowLeft, Calendar, Clock, Hash, Tag, User } from "lucide-react";
import { notFound, useParams } from "next/navigation";
import { projects } from "../_components/data";
import { motion } from "framer-motion";

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const project = projects.find((p) => p.id === projectId);

  if (!project) {
    notFound();
  }

  return (
    <motion.main 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="min-h-screen bg-background text-foreground selection:bg-observer/30"
    >
      <div className="mx-auto w-full max-w-4xl px-6 py-12">
        <Link
          href="/projects"
          className="group mb-8 inline-flex items-center gap-2 rounded-full border border-white/5 bg-white/5 px-4 py-2 text-sm text-foreground-2 transition-colors hover:bg-white/10 hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" />
          Back to projects
        </Link>
        
        <header className="mb-12">
          <div className="mb-4 flex items-center gap-3">
             <span className="rounded-full bg-observer/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-observer-3">
              {project.status}
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-foreground-3">
              {project.id}
            </span>
          </div>
          <h1 className="mb-6 text-5xl font-bold tracking-tight text-white md:text-6xl">
            {project.name}
          </h1>
          <p className="text-xl leading-relaxed text-foreground-2">
            {project.description}
          </p>
        </header>

        <div className="grid gap-8 rounded-3xl border border-white/5 bg-white/5 p-8 backdrop-blur-sm lg:grid-cols-2">
           <div className="space-y-6">
              <h3 className="text-lg font-semibold text-white">Project Details</h3>
              
              <div className="grid gap-4">
                <div className="flex items-center gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-background-3 text-observer-3">
                    <User className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs text-foreground-3">Owner</p>
                    <p className="font-medium text-foreground">{project.owner}</p>
                  </div>
                </div>

                <div className="flex items-center gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-background-3 text-observer-3">
                    <Clock className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs text-foreground-3">Last Update</p>
                    <p className="font-medium text-foreground">{project.lastUpdate}</p>
                  </div>
                </div>

                 <div className="flex items-center gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-background-3 text-observer-3">
                    <Hash className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs text-foreground-3">Current progress</p>
                     <div className="flex items-center gap-3">
                        <span className="font-medium text-foreground">{project.progress}%</span>
                         <div className="h-1.5 w-24 overflow-hidden rounded-full bg-white/10">
                            <div className="h-full bg-observer" style={{ width: `${project.progress}%`}} />
                         </div>
                     </div>
                  </div>
                </div>
              </div>
           </div>

           <div className="space-y-6">
             <h3 className="text-lg font-semibold text-white">Tags & Metadata</h3>
             <div className="flex flex-wrap gap-2">
                {project.tags.map(tag => (
                   <span key={tag} className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-foreground-2">
                      <Tag className="h-3.5 w-3.5 opacity-50" />
                      {tag}
                   </span>
                ))}
             </div>
             
             <div className="mt-8 rounded-2xl bg-observer/5 p-6">
                <p className="mb-2 text-sm font-semibold text-observer-3">Quick Actions</p>
                <div className="space-y-2">
                   <button className="w-full rounded-xl bg-observer px-4 py-3 text-sm font-semibold text-white transition hover:bg-observer-2">
                      Edit Project Details
                   </button>
                   <button className="w-full rounded-xl border border-white/10 bg-transparent px-4 py-3 text-sm font-semibold text-foreground-2 transition hover:bg-white/5 hover:text-white">
                      View Activity Log
                   </button>
                </div>
             </div>
           </div>
        </div>
      </div>
    </motion.main>
  );
}
