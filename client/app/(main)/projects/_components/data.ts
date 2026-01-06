import type { Project } from "./types";

export const projects: Project[] = [
  {
    id: "prj-001",
    name: "Realtime observability",
    description:
      "A live event panel with smart alerts for distributed teams.",
    status: "active",
    owner: "Core Team",
    lastUpdate: "2 hours ago",
    progress: 68,
    tags: ["Realtime", "Analytics", "Core"],
  },
  {
    id: "prj-002",
    name: "Incident view",
    description:
      "Automated prioritization and a critical event timeline.",
    status: "in_review",
    owner: "Ops",
    lastUpdate: "Yesterday",
    progress: 42,
    tags: ["Ops", "Risk"],
  },
  {
    id: "prj-003",
    name: "Room assistant",
    description:
      "Guided flows for fast onboarding and smart room creation.",
    status: "paused",
    owner: "AI",
    lastUpdate: "5 days ago",
    progress: 18,
    tags: ["Onboarding", "AI"],
  },
  {
    id: "prj-004",
    name: "External integrations",
    description:
      "Connectors for third-party tools to orchestrate alerts.",
    status: "active",
    owner: "Integrations",
    lastUpdate: "3 hours ago",
    progress: 76,
    tags: ["API", "Partners"],
  },
  {
    id: "prj-005",
    name: "Access control",
    description:
      "Roles and permissions with advanced audit trails.",
    status: "in_review",
    owner: "Security",
    lastUpdate: "1 day ago",
    progress: 55,
    tags: ["Security", "RBAC"],
  },
  {
    id: "prj-006",
    name: "Health map",
    description:
      "Geographic view to spot degradation in critical services.",
    status: "active",
    owner: "SRE",
    lastUpdate: "6 hours ago",
    progress: 61,
    tags: ["SRE", "Map"],
  },
];
