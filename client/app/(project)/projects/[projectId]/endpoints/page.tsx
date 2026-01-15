"use client";

import { useAnalysis } from "@/hooks/useAnalysis";
import { useProject } from "@/hooks/useProject";
import { notFound, useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Link2, Code, FileCode, Search, Globe } from "lucide-react";
import { useState } from "react";

const getMethodColor = (method: string) => {
  switch (method.toUpperCase()) {
    case "GET": return "text-blue-400 bg-blue-400/10 border-blue-400/20";
    case "POST": return "text-green-400 bg-green-400/10 border-green-400/20";
    case "PUT": return "text-yellow-400 bg-yellow-400/10 border-yellow-400/20";
    case "DELETE": return "text-red-400 bg-red-400/10 border-red-400/20";
    case "PATCH": return "text-purple-400 bg-purple-400/10 border-purple-400/20";
    default: return "text-gray-400 bg-gray-400/10 border-gray-400/20";
  }
};

export default function EndpointsPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const { project, loading: loadingProject } = useProject(projectId);
  const { endpoints, loading: loadingAnalysis } = useAnalysis(projectId);
  const [search, setSearch] = useState("");

  if (loadingProject) {
    return <div className="flex min-h-[60vh] items-center justify-center text-foreground-3">Loading...</div>;
  }

  if (!project) {
    notFound();
    return null;
  }

  const filteredEndpoints = endpoints.filter(e => 
    e.path.toLowerCase().includes(search.toLowerCase()) ||
    e.http_method.toLowerCase().includes(search.toLowerCase()) ||
    e.source_file.toLowerCase().includes(search.toLowerCase()) ||
    (e.source_symbol?.toLowerCase() || "").includes(search.toLowerCase())
  );

  return (
    <motion.main
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Header & Filter */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-observer/10 text-observer">
            <Globe className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">API Endpoints</h1>
            <p className="text-xs text-foreground-3">{endpoints.length} routes detected across the project</p>
          </div>
        </div>

        <div className="relative w-full md:w-72">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-foreground-3" />
          <input
            type="text"
            placeholder="Search endpoints..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-xl border border-white/5 bg-white/5 py-2 pl-9 pr-4 text-sm text-foreground outline-none transition-all focus:border-observer/50 focus:bg-white/10"
          />
        </div>
      </div>

      {/* Endpoints Table/List */}
      <div className="rounded-2xl border border-white/5 bg-white/5 overflow-hidden">
        {loadingAnalysis ? (
           <div className="p-8 text-center text-foreground-3 italic">Discovering endpoints...</div>
        ) : (
          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-bottom border-white/5 bg-white/5 text-[10px] font-bold uppercase tracking-widest text-foreground-3">
                  <th className="px-6 py-4">Method & Route</th>
                  <th className="px-6 py-4">Source Origin</th>
                  <th className="px-6 py-4">Symbol</th>
                  <th className="px-6 py-4 text-right">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredEndpoints.map((endpoint) => (
                  <tr key={endpoint.id} className="group transition-colors hover:bg-white/5">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-4">
                        <span className={`rounded-lg border px-2 py-1 text-[10px] font-bold ${getMethodColor(endpoint.http_method)}`}>
                          {endpoint.http_method}
                        </span>
                        <code className="text-sm font-medium text-white group-hover:text-observer transition-colors">
                          {endpoint.path}
                        </code>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col gap-1">
                        <div className="flex items-center gap-2 text-xs text-foreground">
                           <FileCode className="h-3 w-3 text-foreground-3" />
                           <span className="truncate max-w-[200px]" title={endpoint.source_file}>{endpoint.source_file}</span>
                        </div>
                        <div className="flex items-center gap-2">
                           <span className="text-[10px] font-semibold text-foreground-3 uppercase tracking-tighter">{endpoint.framework}</span>
                           <span className="h-1 w-1 rounded-full bg-white/10" />
                           <span className="text-[10px] font-semibold text-foreground-3 uppercase tracking-tighter">{endpoint.language}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                       <div className="flex items-center gap-2 text-xs font-mono text-foreground-2">
                          <Code className="h-3 w-3 text-foreground-3" />
                          {endpoint.source_symbol || "-"}
                       </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                       <div className="flex items-center justify-end gap-2">
                          <div className="h-1.5 w-16 bg-white/5 rounded-full overflow-hidden">
                             <div 
                                className="h-full bg-observer transition-all duration-500" 
                                style={{ width: `${endpoint.confidence * 100}%` }}
                             />
                          </div>
                          <span className="text-[10px] font-bold text-foreground-3">{(endpoint.confidence * 100).toFixed(0)}%</span>
                       </div>
                    </td>
                  </tr>
                ))}
                {filteredEndpoints.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-6 py-12 text-center text-foreground-3 italic">
                      No endpoints matching your search were found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </motion.main>
  );
}
