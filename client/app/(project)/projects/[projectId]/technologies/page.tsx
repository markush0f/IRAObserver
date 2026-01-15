"use client";

import { useAnalysis } from "@/hooks/useAnalysis";
import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Code, LayoutTemplate, Server } from "lucide-react";
import Image from "next/image";

// Helper for devicon URLs
const getIconUrl = (name: string) => {
  const normalized = name.toLowerCase().replace(".", "").replace("js", "js").replace(" ", "");
  
  // Specific overrides for common mismatches
  const map: Record<string, string> = {
    "c#": "csharp",
    "c++": "cplusplus",
    "next.js": "nextjs",
    "nextjs": "nextjs",
    "node.js": "nodejs",
    "nodejs": "nodejs",
    "react": "react",
    "vue": "vuejs",
    "angular": "angularjs",
    "go": "go",
    "golang": "go",
  };

  const key = map[normalized] || normalized;
  return `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/${key}/${key}-original.svg`;
};

export default function TechnologiesPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject, error: errorProject } = useProject(projectId);
  const { languages, frameworks, infrastructure, loading: loadingAnalysis, error: errorAnalysis } = useAnalysis(projectId);

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

  const sortedLanguages = Object.entries(languages).sort(([, a], [, b]) => b - a);
  const totalLines = sortedLanguages.reduce((acc, [, count]) => acc + count, 0);

  const sortedFrameworks = Object.entries(frameworks).sort(([, a], [, b]) => b - a);

  // Normalize Infrastructure: If both Docker and Docker Compose exist, only show Docker
  const infraNormalized = Array.from(new Set(infrastructure));
  const hasDocker = infraNormalized.some(i => i.toLowerCase() === 'docker');
  const hasDockerCompose = infraNormalized.some(i => i.toLowerCase() === 'docker compose');
  
  const infrastructureToDisplay = (hasDocker && hasDockerCompose) 
    ? infraNormalized.filter(i => i.toLowerCase() !== 'docker compose')
    : infraNormalized;

  return (
    <motion.main
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-transparent text-foreground selection:bg-observer/30"
    >
      <div className="w-full">
         <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            
            {/* Left Column: Languages & Infrastructure */}
            <div className="space-y-6">
               {/* Languages Section */}
               <div className="space-y-4">
                  <div className="flex items-center gap-3">
                     <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                        <Code className="h-5 w-5" />
                     </div>
                     <h2 className="text-xl font-bold text-white">Languages</h2>
                  </div>

                  {loadingAnalysis ? (
                      <p className="text-foreground-3 italic text-sm px-2">Loading languages...</p>
                  ) : (
                      <div className="grid gap-3">
                         {sortedLanguages.map(([lang, count]) => {
                             const percentage = totalLines > 0 ? (count / totalLines) * 100 : 0;
                             return (
                                 <div key={lang} className="group relative overflow-hidden rounded-2xl border border-white/5 bg-white/10 p-4 transition-all hover:bg-white/15">
                                    <div className="flex items-center justify-between z-10 relative">
                                       <div className="flex items-center gap-4">
                                          <div className="relative h-10 w-10 overflow-hidden rounded-xl bg-white/5 p-2 shadow-inner">
                                             <Image 
                                               src={getIconUrl(lang)} 
                                               alt={lang}
                                               fill
                                               className="object-contain p-1.5"
                                               onError={(e) => {
                                                   (e.target as HTMLImageElement).style.display = 'none';
                                                   (e.target as HTMLImageElement).parentElement!.style.backgroundColor = '#3b82f6';
                                               }} 
                                             />
                                          </div>
                                          <div>
                                             <p className="font-semibold text-foreground leading-tight">{lang}</p>
                                             <p className="text-[10px] text-foreground-3 uppercase tracking-wider mt-0.5">{percentage.toFixed(1)}% OF CODEBASE</p>
                                          </div>
                                       </div>
                                       <div className="text-right">
                                          <p className="text-base font-bold text-white tracking-tight">{count.toLocaleString()}</p>
                                          <p className="text-[10px] text-foreground-3 uppercase tracking-widest">LINES</p>
                                       </div>
                                    </div>
                                    <div 
                                       className="absolute bottom-0 left-0 top-0 bg-blue-500/5 transition-all duration-1000 group-hover:bg-blue-500/10" 
                                       style={{ width: `${percentage}%` }}
                                    />
                                 </div>
                             );
                         })}
                         {sortedLanguages.length === 0 && <p className="text-foreground-3 italic text-sm px-2">No languages detected.</p>}
                      </div>
                  )}
               </div>

               {/* Infrastructure Section */}
               <div className="space-y-4 pt-2">
                  <div className="flex items-center gap-3">
                     <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500/10 text-orange-400">
                        <Server className="h-5 w-5" />
                     </div>
                     <h2 className="text-xl font-bold text-white">Infrastructure</h2>
                  </div>

                  {loadingAnalysis ? (
                      <p className="text-foreground-3 italic text-sm px-2">Loading infrastructure...</p>
                  ) : (
                      <div className="grid grid-cols-1 gap-3">
                         {infrastructureToDisplay.map((component) => (
                             <div key={component} className="group relative flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 p-4 transition-all hover:border-observer/30 hover:bg-white/10">
                                <div className="relative h-10 w-10 overflow-hidden rounded-xl bg-white/5 p-2 shadow-inner">
                                   <Image 
                                     src={getIconUrl(component)} 
                                     alt={component}
                                     fill
                                     className="object-contain p-1"
                                     onError={(e) => {
                                         (e.target as HTMLImageElement).style.display = 'none';
                                         (e.target as HTMLImageElement).parentElement!.style.backgroundColor = '#f97316';
                                     }} 
                                   />
                                </div>
                                <div className="flex-1 min-w-0">
                                   <p className="text-sm font-bold text-white uppercase tracking-wider truncate">{component}</p>
                                   <p className="text-[10px] text-foreground-3 font-semibold tracking-widest">DETECTION SYSTEM</p>
                                </div>
                                <div className="absolute -inset-px rounded-2xl bg-gradient-to-br from-observer/0 to-observer/10 opacity-0 transition-opacity group-hover:opacity-100" />
                             </div>
                         ))}
                         {infrastructureToDisplay.length === 0 && <p className="text-foreground-3 italic text-sm px-2">No infrastructure components detected.</p>}
                      </div>
                  )}
               </div>
            </div>

            {/* Right Column: Frameworks */}
            <div className="space-y-4">
               <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                     <LayoutTemplate className="h-5 w-5" />
                  </div>
                  <h2 className="text-xl font-bold text-white">Frameworks</h2>
               </div>

               {loadingAnalysis ? (
                   <p className="text-foreground-3 italic text-sm px-2">Loading frameworks...</p>
               ) : (
                   <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {sortedFrameworks.map(([framework, score]) => (
                          <div key={framework} className="group flex flex-col items-center justify-center gap-4 rounded-3xl border border-white/5 bg-white/5 p-6 text-center transition-all hover:border-observer/30 hover:bg-white/10">
                             <div className="relative h-16 w-16 p-2 rounded-2xl bg-white/5 shadow-2xl transition-transform group-hover:scale-110">
                                 <Image 
                                    src={getIconUrl(framework)} 
                                    alt={framework}
                                    fill
                                    className="object-contain p-3"
                                    onError={(e) => {
                                        (e.target as HTMLImageElement).style.display = 'none';
                                        (e.target as HTMLImageElement).parentElement!.style.backgroundColor = '#7c5ce0';
                                    }}
                                 />
                             </div>
                             <div className="space-y-2">
                                 <h3 className="text-lg font-bold text-white">{framework}</h3>
                                 <span className="inline-flex items-center gap-1.5 rounded-full bg-observer/10 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-observer border border-observer/20">
                                    <span className="h-1.5 w-1.5 rounded-full bg-observer animate-pulse"></span>
                                    Detected
                                 </span>
                             </div>
                          </div>
                      ))}
                      {sortedFrameworks.length === 0 && <p className="col-span-full text-foreground-3 italic text-sm px-2">No frameworks detected.</p>}
                   </div>
               )}
            </div>
            
         </div>
      </div>
    </motion.main>
  );
}
