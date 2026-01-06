import ProjectsGrid from "./_components/ProjectsGrid";
import { projects } from "./_components/data";
import { Filter, Plus } from "lucide-react";

export default function ProjectsPage() {
  return (
    <main className="min-h-screen bg-background text-foreground selection:bg-observer/30">
      <section className="mx-auto w-full max-w-none px-6 py-12">
        <div className="mb-12 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="space-y-1">
            <h2 className="text-4xl font-bold tracking-tight text-white md:text-5xl">
              Projects <span className="text-transparent bg-clip-text bg-gradient-to-r from-observer-3 to-observer">Under Watch</span>
            </h2>
            <p className="mt-2 max-w-2xl text-lg text-foreground-2">
              Track progress, owners, and the operational status of connected
              rooms.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <button
              type="button"
              className="group flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-medium text-foreground-2 transition-all hover:border-white/20 hover:bg-white/10 hover:text-white"
            >
              <Filter className="h-4 w-4" />
              <span>Filter</span>
            </button>
            <button
              type="button"
              className="group relative flex items-center gap-2 overflow-hidden rounded-full bg-observer px-6 py-2.5 text-sm font-semibold text-white shadow-[0_0_20px_rgba(124,92,224,0.3)] transition-all hover:bg-observer-2 hover:shadow-[0_0_30px_rgba(124,92,224,0.5)]"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
              <Plus className="h-4 w-4" />
              <span>Create project</span>
            </button>
          </div>
        </div>
        <ProjectsGrid projects={projects} />
      </section>
    </main>
  );
}
