export type ProjectStatus = "active" | "in_review" | "paused";

export type Project = {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  owner: string;
  lastUpdate: string;
  progress: number;
  tags: string[];
};
