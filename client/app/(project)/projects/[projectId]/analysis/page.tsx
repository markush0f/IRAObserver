"use client";

import { useAnalysis } from "@/hooks/useAnalysis";
import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Code, LayoutTemplate } from "lucide-react";
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

export default function AnalysisPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject, error: errorProject } = useProject(projectId);
  const { languages, frameworks, loading: loadingAnalysis, error: errorAnalysis } = useAnalysis(projectId);

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

  return (
    <motion.main
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-transparent text-foreground selection:bg-observer/30"
    >
      <div className="w-full space-y-8">
         {/* No header as requested previously in other views, keeping consistence */}
         
         <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            
            {/* Languages Section */}
            <div className="space-y-6">
               <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                     <Code className="h-5 w-5" />
                  </div>
                  <h2 className="text-xl font-bold text-white">Languages</h2>
               </div>

               {loadingAnalysis ? (
                   <p className="text-foreground-3">Loading languages...</p>
               ) : (
                   <div className="grid gap-4">
                      {sortedLanguages.map(([lang, count]) => {
                          const percentage = totalLines > 0 ? (count / totalLines) * 100 : 0;
                          return (
                              <div key={lang} className="group relative overflow-hidden rounded-2xl border border-white/5 bg-white/5 p-4 transition-all hover:bg-white/10">
                                 <div className="flex items-center justify-between z-10 relative">
                                    <div className="flex items-center gap-3">
                                       <div className="relative h-8 w-8 overflow-hidden rounded-lg bg-white/5 p-1">
                                          <Image 
                                            src={getIconUrl(lang)} 
                                            alt={lang}
                                            fill
                                            className="object-contain"
                                            onError={(e) => {
                                                // Fallback if image fails (using a colored box)
                                                (e.target as HTMLImageElement).style.display = 'none';
                                                (e.target as HTMLImageElement).parentElement!.style.backgroundColor = '#3b82f6';
                                            }} 
                                          />
                                       </div>
                                       <span className="font-semibold text-foreground">{lang}</span>
                                    </div>
                                    <div className="text-right">
                                       <p className="text-sm font-bold text-white">{count.toLocaleString()} lines</p>
                                       <p className="text-xs text-foreground-3">{percentage.toFixed(1)}%</p>
                                    </div>
                                 </div>
                                 {/* Progress Bar Background */}
                                 <div 
                                    className="absolute bottom-0 left-0 top-0 bg-blue-500/5 transition-all duration-1000 group-hover:bg-blue-500/10" 
                                    style={{ width: `${percentage}%` }}
                                 />
                              </div>
                          );
                      })}
                      {sortedLanguages.length === 0 && <p className="text-foreground-3">No languages detected.</p>}
                   </div>
               )}
            </div>

            {/* Frameworks Section */}
            <div className="space-y-6">
               <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                     <LayoutTemplate className="h-5 w-5" />
                  </div>
                  <h2 className="text-xl font-bold text-white">Frameworks</h2>
               </div>

               {loadingAnalysis ? (
                   <p className="text-foreground-3">Loading frameworks...</p>
               ) : (
                   <div className="grid grid-cols-2 gap-4">
                      {sortedFrameworks.map(([framework, score]) => {
                          const percentage = score * 100;
                          return (
                              <div key={framework} className="flex flex-col items-center justify-center gap-4 rounded-2xl border border-white/5 bg-white/5 p-6 text-center transition-all hover:border-observer/30 hover:bg-white/10">
                                 <div className="relative h-16 w-16 p-2 rounded-2xl bg-white/5 shadow-inner">
                                     <Image 
                                        src={getIconUrl(framework)} 
                                        alt={framework}
                                        fill
                                        className="object-contain p-2"
                                        onError={(e) => {
                                            (e.target as HTMLImageElement).style.display = 'none';
                                            (e.target as HTMLImageElement).parentElement!.style.backgroundColor = '#7c5ce0';
                                        }}
                                     />
                                 </div>
                                 <div>
                                     <h3 className="font-bold text-white">{framework}</h3>
                                     <span className="mt-1 inline-block rounded-full bg-observer/10 px-2 py-0.5 text-xs font-medium text-observer">
                                        Detected
                                     </span>
                                 </div>
                              </div>
                          );
                      })}
                      {sortedFrameworks.length === 0 && <p className="col-span-2 text-foreground-3">No frameworks detected.</p>}
                   </div>
               )}
            </div>

         </div>
      </div>
    </motion.main>
  );
}
