"use client";

import { Clock, Hash, Tag, User, GitCommit } from "lucide-react";
import { notFound, useParams } from "next/navigation";
import { ProjectMember } from "@/types/project";
import { Snapshot } from "@/types/snapshot";
import { useProject } from "@/hooks/useProject";
import { useSnapshots } from "@/hooks/useSnapshots";
import { useProjectMembers } from "@/hooks/useProjectMembers";
import { motion } from "framer-motion";
import Image from "next/image";

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject, error: errorProject } = useProject(projectId);
  const { snapshots, loading: loadingSnapshots } = useSnapshots(projectId);
  const { members, loading: loadingMembers } = useProjectMembers(projectId);

  if (loadingProject) {
    return (
      <div className="flex min-h-screen items-center justify-center text-foreground-3">
        Loading project details...
      </div>
    );
  }

  if (errorProject || !project) {
    if (errorProject) console.error(errorProject);
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
            


            {/* Source Configuration Block */}
            <div className="space-y-4">
               <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground-3">Source Configuration</h3>
               <div className="group relative overflow-hidden rounded-xl bg-[#0b0f16] border border-white/10 p-4 transition-colors hover:border-observer/30">
                  <div className="flex items-start gap-3">
                     <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded bg-white/5 text-foreground-2">
                        <Tag className="h-3.5 w-3.5" />
                     </div>
                     <div className="space-y-0.5 min-w-0 flex-1">
                        <p className="text-[11px] text-foreground-3">Repository URL</p>
                        <a 
                          href={project.source_ref}
                          target="_blank"
                          rel="noopener noreferrer" 
                          className="block truncate font-mono text-xs text-observer hover:underline underline-offset-4"
                        >
                           {project.source_ref}
                        </a>
                     </div>
                  </div>
               </div>
            </div>



             {/* Activity / Timeline Block */}
            <div className="space-y-4">
               <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground-3">Lifecycle & Snapshots</h3>
               <div className="max-h-[400px] overflow-y-auto pr-4 custom-scrollbar">
                  <div className="relative border-l border-white/10 pl-6 space-y-8 ml-2 mt-2 pb-4">
                     <div className="relative">
                        <span className="absolute -left-[30px] top-1 h-3 w-3 rounded-full border-2 border-[#0b0f16] bg-observer shadow-[0_0_10px_rgba(124,92,224,0.5)]"></span>
                        <p className="text-sm text-foreground-3 mb-1">Project Created</p>
                        <p className="text-lg font-medium text-foreground">
                           {new Date(project.created_at).toLocaleDateString(undefined, { dateStyle: 'long' })}
                        </p>
                     </div>

                     {loadingSnapshots ? (
                        <div className="text-sm text-foreground-3">Loading snapshots...</div>
                     ) : snapshots.length > 0 ? (
                        snapshots.map((snapshot: Snapshot) => (
                           <div key={snapshot.id} className="relative group">
                           <span className="absolute -left-[30px] top-1 h-3 w-3 rounded-full border-2 border-[#0b0f16] bg-white/20 group-hover:bg-white transition-colors group-hover:shadow-[0_0_10px_rgba(255,255,255,0.5)]"></span>
                           <div className="flex flex-col gap-1">
                              <div className="flex items-center gap-2">
                                 <p className="text-sm font-medium text-foreground group-hover:text-white transition-colors">
                                    Snapshot Analyzed
                                 </p>
                                 {snapshot.commit_hash && (
                                    <span className="flex items-center gap-1 rounded bg-white/5 px-1.5 py-0.5 font-mono text-[10px] text-foreground-3">
                                    <GitCommit className="h-3 w-3" />
                                    {snapshot.commit_hash.substring(0, 7)}
                                    </span>
                                 )}
                              </div>
                              <p className="text-xs text-foreground-3">
                                 {new Date(snapshot.created_at).toLocaleString()}
                              </p>
                           </div>
                           </div>
                        ))
                     ) : (
                        <div className="relative">
                           <span className="absolute -left-[30px] top-1 h-3 w-3 rounded-full border-2 border-[#0b0f16] bg-white/10"></span>
                           <p className="text-sm text-foreground-3">No snapshots recorded yet.</p>
                        </div>
                     )}
                  </div>
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
                
                <div className="space-y-4">
                   <div className="space-y-1">
                      <h2 className="text-2xl font-bold text-white tracking-tight leading-tight">
                         {project.name}
                      </h2>
                      <p className="text-[10px] text-foreground-3 font-semibold uppercase tracking-widest opacity-60">Project Identity</p>
                   </div>

                   <div className="pt-2 flex flex-col items-center gap-2">
                      <p className="text-[10px] text-foreground-3 font-medium uppercase tracking-wider">Current Status</p>
                      {project.last_analysis_at ? (
                        <div className="inline-flex items-center gap-2 rounded-full bg-green-500/10 px-4 py-1 text-green-400 border border-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.1)]">
                           <span className="relative flex h-2 w-2">
                             <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                             <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                           </span>
                           <span className="font-bold text-xs">Active & Analyzed</span>
                        </div>
                      ) : (
                        <div className="inline-flex items-center gap-2 rounded-full bg-yellow-500/10 px-4 py-1 text-yellow-400 border border-yellow-500/20 shadow-[0_0_15px_rgba(234,179,8,0.1)]">
                           <span className="h-2 w-2 rounded-full bg-yellow-500" />
                           <span className="font-bold text-xs">Pending Analysis</span>
                        </div>
                      )}
                   </div>
                </div>
             </div>

             {/* Team Members Block */}
             <div className="space-y-4">
                <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground-3 px-2">Team Members</h3>
                <div className="flex flex-col gap-3">
                   {loadingMembers ? (
                      <div className="py-4 text-sm text-foreground-3 italic px-2">Loading team members...</div>
                   ) : members.length > 0 ? (
                      members.map((member: ProjectMember) => (
                         <div key={member.id} className="flex items-center gap-3 rounded-2xl bg-white/5 border border-white/10 p-3 transition-colors hover:border-observer/30 group">
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-observer/10 text-observer ring-1 ring-observer/20">
                               <User className="h-4 w-4" />
                            </div>
                            <div className="min-w-0 flex-1">
                               <p className="truncate text-sm font-semibold text-foreground group-hover:text-observer transition-colors">
                                  {member.user.display_name}
                               </p>
                               <p className="text-[10px] uppercase tracking-wider text-foreground-3">
                                  {member.role === 'admin' ? 'Administrator' : 'Contributor'}
                               </p>
                            </div>
                            {member.user.role === 'admin' && (
                               <div className="h-1.5 w-1.5 rounded-full bg-observer shadow-[0_0_8px_rgba(124,92,224,0.8)]" title="System Admin" />
                            )}
                         </div>
                      ))
                   ) : (
                      <div className="py-4 text-sm text-foreground-3 italic px-2">No team members assigned.</div>
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
