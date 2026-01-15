"use client";

import { useAnalysis } from "@/hooks/useAnalysis";
import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Code, LayoutTemplate, Server, Package, FileCode, Hash, ChevronRight } from "lucide-react";
import Image from "next/image";
import { getIconUrl } from "@/lib/utils/icons";

export default function TechnologiesPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject, error: errorProject } = useProject(projectId);
  const { languages, frameworks, infrastructure, dependencies, loading: loadingAnalysis } = useAnalysis(projectId);

  if (loadingProject) {
    return <div className="flex min-h-[60vh] items-center justify-center text-foreground-3">Loading...</div>;
  }

  if (errorProject || !project) {
     if (errorProject) console.error(errorProject);
     notFound();
     return null;
  }

  const sortedLanguages = Object.entries(languages).sort(([, a], [, b]) => b - a);
  const totalLines = sortedLanguages.reduce((acc, [, count]) => acc + count, 0);
  const sortedFrameworks = Object.entries(frameworks).sort(([, a], [, b]) => b - a);

  const infraNormalized = Array.from(new Set(infrastructure));
  const hasDocker = infraNormalized.some(i => i.toLowerCase() === 'docker');
  const hasDockerCompose = infraNormalized.some(i => i.toLowerCase() === 'docker compose');
  const infrastructureToDisplay = (hasDocker && hasDockerCompose) 
    ? infraNormalized.filter(i => i.toLowerCase() !== 'docker compose')
    : infraNormalized;

  const groupedDeps = dependencies.reduce((acc, dep) => {
      if (!acc[dep.source_file]) acc[dep.source_file] = [];
      acc[dep.source_file].push(dep);
      return acc;
  }, {} as Record<string, typeof dependencies>);

  return (
    <motion.main
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-transparent text-foreground selection:bg-observer/30"
    >
      <div className="w-full">
         <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
            
            {/* Left Column (Stack Details) - 5/12 width */}
            <div className="space-y-6 lg:col-span-5">
               
               {/* Languages */}
               <div className="space-y-3">
                  <div className="flex items-center gap-3">
                     <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
                        <Code className="h-4 w-4" />
                     </div>
                     <h2 className="text-sm font-bold text-white uppercase tracking-wider">Languages</h2>
                  </div>
                  <div className="grid gap-2">
                     {sortedLanguages.map(([lang, count]) => {
                         const percentage = totalLines > 0 ? (count / totalLines) * 100 : 0;
                         return (
                             <div key={lang} className="group relative overflow-hidden rounded-xl border border-white/5 bg-white/5 p-2.5 transition-all hover:bg-white/10">
                                <div className="flex items-center justify-between z-10 relative">
                                   <div className="flex items-center gap-3">
                                      <div className="relative h-7 w-7 overflow-hidden rounded-md bg-white/5 p-1 shadow-inner">
                                         <Image src={getIconUrl(lang)} alt={lang} fill className="object-contain p-0.5" onError={(e) => { (e.target as any).style.display = 'none'; (e.target as any).parentElement.style.backgroundColor = '#3b82f6'; }} />
                                      </div>
                                      <div>
                                         <p className="font-semibold text-foreground text-xs">{lang}</p>
                                         <p className="text-[8px] text-foreground-3 uppercase tracking-wider">{percentage.toFixed(1)}%</p>
                                      </div>
                                   </div>
                                   <div className="text-right">
                                      <p className="text-xs font-bold text-white leading-none">{count.toLocaleString()}</p>
                                      <p className="text-[8px] text-foreground-3 uppercase tracking-widest mt-0.5">LINES</p>
                                   </div>
                                </div>
                                <div className="absolute bottom-0 left-0 top-0 bg-blue-500/5 transition-all duration-1000 group-hover:bg-blue-500/10" style={{ width: `${percentage}%` }} />
                             </div>
                         );
                     })}
                  </div>
               </div>

               {/* Infrastructure */}
               <div className="space-y-3">
                  <div className="flex items-center gap-3">
                     <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-500/10 text-orange-400">
                        <Server className="h-4 w-4" />
                     </div>
                     <h2 className="text-sm font-bold text-white uppercase tracking-wider">Infrastructure</h2>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                     {infrastructureToDisplay.map((component) => (
                         <div key={component} className="flex items-center gap-3 rounded-xl border border-white/5 bg-white/5 p-2">
                            <div className="relative h-6 w-6 overflow-hidden rounded bg-white/5 p-1 flex-shrink-0">
                               <Image src={getIconUrl(component)} alt={component} fill className="object-contain" onError={(e) => { (e.target as any).style.display = 'none'; (e.target as any).parentElement.style.backgroundColor = '#f97316'; }} />
                            </div>
                            <div className="min-w-0">
                               <p className="text-[10px] font-bold text-white uppercase tracking-wider truncate">{component}</p>
                            </div>
                         </div>
                     ))}
                  </div>
               </div>

               {/* Frameworks */}
               <div className="space-y-3">
                  <div className="flex items-center gap-3">
                     <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-500/10 text-purple-400">
                        <LayoutTemplate className="h-4 w-4" />
                     </div>
                     <h2 className="text-sm font-bold text-white uppercase tracking-wider">Frameworks</h2>
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                     {sortedFrameworks.map(([framework]) => (
                         <div key={framework} className="flex flex-col items-center justify-center gap-2 rounded-xl border border-white/5 bg-white/5 p-3 text-center hover:bg-white/10 transition-colors">
                            <div className="relative h-8 w-8 p-1 rounded-lg bg-white/5">
                                <Image src={getIconUrl(framework)} alt={framework} fill className="object-contain p-1" onError={(e) => { (e.target as any).style.display = 'none'; (e.target as any).parentElement.style.backgroundColor = '#7c5ce0'; }} />
                            </div>
                            <p className="text-[9px] font-bold text-white truncate w-full">{framework}</p>
                         </div>
                     ))}
                  </div>
               </div>
            </div>

            {/* Right Column (Dependencies) - 7/12 width */}
            <div className="lg:col-span-7 space-y-4">
               <div className="flex items-center gap-3 mb-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-500/10 text-green-400">
                     <Package className="h-4 w-4" />
                  </div>
                  <div>
                     <h2 className="text-sm font-bold text-white uppercase tracking-wider">Dependencies</h2>
                     <p className="text-[9px] text-foreground-3 uppercase tracking-widest">{dependencies.length} packages found</p>
                  </div>
               </div>

               <div className="space-y-4">
                  {Object.entries(groupedDeps).map(([file, deps]) => (
                     <div key={file} className="overflow-hidden rounded-xl border border-white/5 bg-black/40 shadow-xl">
                        <div className="flex items-center gap-2 border-b border-white/5 bg-white/5 px-4 py-2">
                           <FileCode className="h-3.5 w-3.5 text-foreground-3" />
                           <span className="font-mono text-[11px] font-bold text-foreground-2">{file}</span>
                        </div>
                        <div className="max-h-[calc(100vh-100px)] overflow-y-auto custom-scrollbar p-1">
                           <div className="space-y-px font-mono">
                              {deps.map((dep, idx) => (
                                 <div key={dep.id} className="group flex items-center gap-3 rounded px-3 py-1 hover:bg-white/5 transition-colors">
                                    <span className="w-5 text-right text-[9px] font-medium text-white/10 select-none">{(idx + 1)}</span>
                                    <div className="flex flex-1 items-center justify-between gap-2 overflow-hidden">
                                       <span className="text-[11px] font-bold text-observer truncate group-hover:text-white transition-colors">{dep.name}</span>
                                       <div className="flex items-center gap-3 flex-shrink-0">
                                          <span className="text-[10px] font-medium text-foreground-3 whitespace-nowrap">{dep.version}</span>
                                          <span className={`rounded-sm px-1 py-0.5 text-[7px] font-bold uppercase ${dep.scope === 'runtime' ? 'bg-green-500/10 text-green-400' : 'bg-blue-500/10 text-blue-400'}`}>
                                             {dep.scope.substring(0, 3)}
                                          </span>
                                       </div>
                                    </div>
                                 </div>
                              ))}
                           </div>
                        </div>
                     </div>
                  ))}
               </div>
            </div>
            
         </div>
      </div>
    </motion.main>
  );
}
