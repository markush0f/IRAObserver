
import { useState, useEffect, useCallback } from "react";
import { ProjectMember } from "../types/project";
import { projectService } from "../services/ProjectService";

export function useProjectMembers(projectId: string | undefined | null) {
    const [members, setMembers] = useState<ProjectMember[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchMembers = useCallback(async () => {
        if (!projectId) return;

        setLoading(true);
        setError(null);
        try {
            const data = await projectService.getMembers(projectId);
            setMembers(data);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch project members";
            setError(message);
        } finally {
            setLoading(false);
        }
    }, [projectId]);

    useEffect(() => {
        if (projectId) {
            fetchMembers();
        } else {
            setLoading(false);
        }
    }, [projectId, fetchMembers]);

    return { members, loading, error, refetch: fetchMembers };
}
