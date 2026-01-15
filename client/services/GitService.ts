
import { apiClient } from "../lib/api-client";
import { GitBranch, GitCommit } from "../types/git";

export class GitService {
    async getBranches(projectId: string): Promise<GitBranch[]> {
        return apiClient.get<GitBranch[]>(`/projects/${projectId}/git/branches`);
    }

    async getCommits(projectId: string, limit: number = 20, since?: string, until?: string): Promise<GitCommit[]> {
        let url = `/projects/${projectId}/git/commits?limit=${limit}`;
        if (since) url += `&since=${since}`;
        if (until) url += `&until=${until}`;
        return apiClient.get<GitCommit[]>(url);
    }

    async getActiveBranch(projectId: string): Promise<{ branch: string }> {
        return apiClient.get<{ branch: string }>(`/projects/${projectId}/git/branch`);
    }
}

export const gitService = new GitService();
