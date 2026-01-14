
import { useState, useEffect, useCallback } from "react";
import { Project } from "../types/project";
import { projectService } from "../services/ProjectService";

export function useProject(id: string | undefined | null) {
    const [project, setProject] = useState<Project | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchProject = useCallback(async () => {
        if (!id) return;

        setLoading(true);
        setError(null);
        try {
            const data = await projectService.getById(id);
            setProject(data);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch project";
            setError(message);
        } finally {
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            fetchProject();
        } else {
            setLoading(false);
        }
    }, [id, fetchProject]);

    return { project, loading, error, refetch: fetchProject };
}
