
import { useState, useEffect, useCallback } from "react";
import { Project } from "../types/project";
import { projectService } from "../services/ProjectService";

export function useProjects() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchProjects = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await projectService.getAll();
            setProjects(data);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch projects";
            setError(message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchProjects();
    }, [fetchProjects]);

    return { projects, loading, error, refetch: fetchProjects };
}
