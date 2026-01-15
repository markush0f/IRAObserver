"use client";

import { useGit } from "@/hooks/useGit";
import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { GitBranchIcon, GitCommit, GitPullRequest, User, Calendar } from "lucide-react";
import { motion } from "framer-motion";

export default function GitPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject, error: errorProject } = useProject(projectId);
  const { branches, commits, loadingBranches, loadingCommits } = useGit(projectId);

  if (loadingProject) {
    return (
        <div className="flex min-h-screen items-center justify-center text-foreground-3">
            Loading...
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
      <div className="w-full space-y-8">
         <header className="flex flex-col gap-4 border-b border-white/10 pb-6">
            <h1 className="text-4xl font-bold tracking-tight text-white">Repository</h1>
            <p className="text-foreground-2">
                Manage and view git data for <span className="font-semibold text-white">{project.name}</span>
            </p>
         </header>

         <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
            {/* Commits Section */}
            <div className="lg:col-span-2 space-y-6">
               <h2 className="flex items-center gap-2 text-xl font-semibold text-white">
                 <GitCommit className="h-5 w-5 text-observer" />
                 Recent Commits
               </h2>

               {loadingCommits ? (
                  <div className="text-sm text-foreground-3">Loading commits...</div>
               ) : (
                  <div className="space-y-4">
                     {commits.map((commit) => (
                        <div key={commit.commit_hash} className="group relative rounded-2xl border border-white/5 bg-white/5 p-5 transition-all hover:bg-white/10 hover:border-white/10">
                           <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                              <div className="space-y-1">
                                 <p className="font-medium text-foreground group-hover:text-white transition-colors">
                                    {commit.message}
                                 </p>
                                 <div className="flex items-center gap-3 text-xs text-foreground-3">
                                     <span className="flex items-center gap-1">
                                        <User className="h-3 w-3" />
                                        {commit.author_name}
                                     </span>
                                     <span className="flex items-center gap-1">
                                        <Calendar className="h-3 w-3" />
                                        {new Date(commit.authored_at).toLocaleString()}
                                     </span>
                                 </div>
                              </div>
                              <div className="shrink-0 font-mono text-xs text-observer bg-observer/10 px-2 py-1 rounded">
                                 {commit.commit_hash.substring(0, 7)}
                              </div>
                           </div>
                        </div>
                     ))}
                     
                     {commits.length === 0 && (
                        <p className="text-foreground-3">No commits found.</p>
                     )}
                  </div>
               )}
            </div>

            {/* Branches Section */}
            <div className="space-y-6">
                <h2 className="flex items-center gap-2 text-xl font-semibold text-white">
                  <GitBranchIcon className="h-5 w-5 text-green-400" />
                  Branches
                </h2>

                {loadingBranches ? (
                    <div className="text-sm text-foreground-3">Loading branches...</div>
                ) : (
                    <div className="rounded-2xl border border-white/5 bg-white/5 p-2">
                       {branches.map((branch, idx) => (
                          <div key={idx} className="flex items-center gap-3 rounded-xl px-4 py-3 transition hover:bg-white/5">
                             <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-500/10 text-green-400">
                                <GitBranchIcon className="h-4 w-4" />
                             </div>
                             <span className="text-sm font-medium text-foreground truncate" title={typeof branch === 'string' ? branch : ''}>
                                {typeof branch === 'string' ? branch : JSON.stringify(branch)}
                             </span>
                          </div>
                       ))}
                       {branches.length === 0 && (
                          <div className="p-4 text-center text-sm text-foreground-3">No branches found.</div>
                       )}
                    </div>
                )}

                {/* Quick actions or repo info could go here */}
                <div className="rounded-2xl border border-white/5 bg-[#0b0f16] p-6 space-y-4">
                    <h3 className="text-sm font-medium text-foreground-2 uppercase tracking-wider">Repository Source</h3>
                    <div className="flex items-center gap-2 text-sm text-observer break-all">
                       <GitPullRequest className="h-4 w-4 shrink-0" />
                       <a href={project.source_ref} target="_blank" rel="noopener noreferrer" className="hover:underline underline-offset-4">
                          {project.source_ref}
                       </a>
                    </div>
                </div>
            </div>
         </div>
      </div>
    </motion.main>
  );
}
