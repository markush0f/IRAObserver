import type { ProjectStatus } from "./types";

const statusStyles: Record<ProjectStatus, string> = {
  active: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_10px_rgba(52,211,153,0.15)]",
  in_review: "bg-amber-500/10 text-amber-400 border-amber-500/20 shadow-[0_0_10px_rgba(251,191,36,0.15)]",
  paused: "bg-rose-500/10 text-rose-400 border-rose-500/20 shadow-[0_0_10px_rgba(251,113,133,0.15)]",
};

const statusLabel: Record<ProjectStatus, string> = {
  active: "Active",
  in_review: "In review",
  paused: "Paused",
};

export default function StatusBadge({ status }: { status: ProjectStatus }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
        statusStyles[status]
      }`}
    >
      <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-current" />
      {statusLabel[status]}
    </span>
  );
}
