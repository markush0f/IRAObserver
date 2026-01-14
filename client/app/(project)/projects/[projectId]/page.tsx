"use client";

import { Clock, Hash, Tag, User } from "lucide-react";
import { notFound, useParams } from "next/navigation";
import { useProject } from "@/hooks/useProject";
import { motion } from "framer-motion";
import Image from "next/image";

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading, error } = useProject(projectId);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-foreground-3">
        Loading project details...
      </div>
    );
  }

  if (error || !project) {
    if (error) console.error(error);
    notFound(); 
    return null; 
  }

  return (
    <motion.main 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-transparent text-foreground selection:bg-observer/30"
    >
      <div className="w-full">
        
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-3">
          {/* Main Content Area (Left) */}
          <div className="lg:col-span-2 space-y-12">
            
            {/* Header Info */}
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                 <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-foreground-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-observer"></span>
                    {project.source_type.toUpperCase()}
                 </span>
                 <span className="text-xs font-mono text-foreground-3 opacity-50">
                    ID: {project.id}
                 </span>
              </div>
              
              <h1 className="text-5xl font-bold tracking-tight text-white md:text-7xl">
                {project.name}
              </h1>
              
              <p className="text-xl text-foreground-2 leading-relaxed max-w-2xl">
                {project.description}
              </p>
            </div>

            {/* Source Configuration Block */}
            <div className="space-y-4">
               <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground-3">Source Configuration</h3>
               <div className="group relative overflow-hidden rounded-2xl bg-[#0b0f16] border border-white/10 p-6 transition-colors hover:border-observer/30">
                  <div className="flex items-start gap-4">
                     <div className="mt-1 flex h-8 w-8 items-center justify-center rounded bg-white/5 text-foreground-2">
                        <Tag className="h-4 w-4" />
                     </div>
                     <div className="space-y-1 min-w-0 flex-1">
                        <p className="text-sm text-foreground-3">Repository URL</p>
                        <a 
                          href={project.source_ref}
                          target="_blank"
                          rel="noopener noreferrer" 
                          className="block truncate font-mono text-sm text-observer hover:underline underline-offset-4"
                        >
                           {project.source_ref}
                        </a>
                     </div>
                  </div>
               </div>
            </div>

             {/* Activity / Timeline Block */}
            <div className="space-y-4">
               <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground-3">Lifecycle</h3>
               <div className="relative border-l border-white/10 pl-6 space-y-8 ml-2">
                  <div className="relative">
                     <span className="absolute -left-[29px] top-1 h-3 w-3 rounded-full border-2 border-[#0b0f16] bg-observer"></span>
                     <p className="text-sm text-foreground-3 mb-1">Created on</p>
                     <p className="text-lg font-medium text-foreground">
                        {new Date(project.created_at).toLocaleDateString(undefined, { dateStyle: 'long' })}
                     </p>
                  </div>
                  {project.last_analysis_at && (
                    <div className="relative">
                       <span className="absolute -left-[29px] top-1 h-3 w-3 rounded-full border-2 border-[#0b0f16] bg-green-500"></span>
                       <p className="text-sm text-foreground-3 mb-1">Last Analysis</p>
                       <p className="text-lg font-medium text-foreground">
                          {new Date(project.last_analysis_at).toLocaleDateString(undefined, { dateStyle: 'long' })}
                       </p>
                    </div>
                  )}
               </div>
            </div>
          </div>

          {/* Sidebar Context (Right) */}
          <aside className="lg:col-span-1 space-y-8">
             {/* Identity Card */}
             <div className="rounded-3xl bg-white/5 p-8 border border-white/5 flex flex-col items-center text-center gap-6">
                <div className="relative h-40 w-40 rounded-full border-4 border-white/5 shadow-2xl overflow-hidden">
                    <Image 
                      src="/project-placeholder.png" 
                      alt="Project Icon" 
                      fill
                      className="object-cover"
                    />
                </div>
                
                <div className="space-y-2">
                   <p className="text-sm text-foreground-3 font-medium uppercase tracking-wider">Current Status</p>
                   {project.last_analysis_at ? (
                     <div className="inline-flex items-center gap-2 rounded-full bg-green-500/10 px-4 py-1.5 text-green-400 border border-green-500/20">
                        <span className="relative flex h-2.5 w-2.5">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
                        </span>
                        <span className="font-bold text-sm">Active & Analyzed</span>
                     </div>
                   ) : (
                     <div className="inline-flex items-center gap-2 rounded-full bg-yellow-500/10 px-4 py-1.5 text-yellow-400 border border-yellow-500/20">
                        <span className="h-2.5 w-2.5 rounded-full bg-yellow-500" />
                        <span className="font-bold text-sm">Pending Analysis</span>
                     </div>
                   )}
                </div>
             </div>

             {/* Actions removed as requested */}
          </aside>

        </div>
      </div>
    </motion.main>
  );
}
