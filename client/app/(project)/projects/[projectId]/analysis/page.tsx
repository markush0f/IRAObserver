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
      <div className="flex h-[60vh] flex-col items-center justify-center space-y-4 text-center">
         <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5 border border-white/10 text-foreground-3">
            <LayoutTemplate className="h-8 w-8" />
         </div>
         <div className="space-y-1">
            <h2 className="text-xl font-bold text-white">Advanced Analysis</h2>
            <p className="text-sm text-foreground-3 max-w-xs"> Detailed vulnerability and architectural analysis will be available here soon. </p>
         </div>
      </div>
    </motion.main>
  );
}
