
import { apiClient } from "../lib/api-client";
import { Project, ProjectMember } from "../types/project";

export class ProjectService {
    async getAll(): Promise<Project[]> {
        return apiClient.get<Project[]>("/projects");
    }

    async getById(id: string): Promise<Project> {
        return apiClient.get<Project>(`/projects/${id}`);
    }

    async create(data: Omit<Project, "id">): Promise<Project> {
        return apiClient.post<Project>("/projects", data);
    }

    async update(id: string, data: Partial<Project>): Promise<Project> {
        return apiClient.put<Project>(`/projects/${id}`, data);
    }

    async getMembers(id: string): Promise<ProjectMember[]> {
        return apiClient.get<ProjectMember[]>(`/projects/${id}/members`);
    }

    async delete(id: string): Promise<void> {
        return apiClient.delete<void>(`/projects/${id}`);
    }
}

export const projectService = new ProjectService();
