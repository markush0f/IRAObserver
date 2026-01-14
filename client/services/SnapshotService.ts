
import { apiClient } from "../lib/api-client";
import { SnapshotResponse } from "../types/snapshot";

export class SnapshotService {
    async getCompact(projectId: string, limit: number = 100, offset: number = 0): Promise<SnapshotResponse> {
        return apiClient.get<SnapshotResponse>(`/projects/${projectId}/snapshots/compact?limit=${limit}&offset=${offset}`);
    }
}

export const snapshotService = new SnapshotService();
