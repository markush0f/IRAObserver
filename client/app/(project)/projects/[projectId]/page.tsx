"use client";

import { Clock, Hash, Tag, User } from "lucide-react";
import { notFound, useParams } from "next/navigation";
import { useProject } from "@/hooks/useProject";
import { motion } from "framer-motion";

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
    return null; // Ensure we return null after notFound triggers (though next handles it)
  }

  return (
    <motion.main 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="min-h-screen bg-transparent text-foreground selection:bg-observer/30"
    >
      <div className="mx-auto w-full max-w-5xl">        
        <header className="mb-12">
          <div className="mb-4 flex items-center gap-3">
             <span className="rounded-full bg-observer/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-observer-3">
              {project.source_type}
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-foreground-3">
              {project.id.split("-")[0]}...
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
                    <p className="text-xs text-foreground-3">Source Ref</p>
                    <p className="font-medium text-foreground truncate max-w-[200px]" title={project.source_ref}>
                        {project.source_ref}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-background-3 text-observer-3">
                    <Clock className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs text-foreground-3">Created At</p>
                    <p className="font-medium text-foreground">
                        {new Date(project.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                 <div className="flex items-center gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-background-3 text-observer-3">
                    <Hash className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs text-foreground-3">Analysis Status</p>
                    <p className="font-medium text-foreground">
                        {project.last_analysis_at ? 'Analyzed' : 'Pending'}
                    </p>
                  </div>
                </div>
              </div>
           </div>

           <div className="space-y-6">
             <h3 className="text-lg font-semibold text-white">Metadata</h3>
             <div className="flex flex-wrap gap-2">
                {/* Placeholder for tags if they come back later */}
                 <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-foreground-2">
                      <Tag className="h-3.5 w-3.5 opacity-50" />
                      {project.source_type}
                 </span>
             </div>
             
             <div className="mt-8 rounded-2xl bg-observer/5 p-6">
                <p className="mb-2 text-sm font-semibold text-observer-3">Quick Actions</p>
                <div className="space-y-2">
                   <button className="w-full rounded-xl bg-observer px-4 py-3 text-sm font-semibold text-white transition hover:bg-observer-2">
                      Analyze Project
                   </button>
                   <button className="w-full rounded-xl border border-white/10 bg-transparent px-4 py-3 text-sm font-semibold text-foreground-2 transition hover:bg-white/5 hover:text-white">
                      View Source
                   </button>
                </div>
             </div>
           </div>
        </div>
      </div>
    </motion.main>
  );
}
