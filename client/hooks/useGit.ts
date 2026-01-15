
import { useState, useEffect, useCallback } from "react";
import { GitBranch, GitCommit } from "../types/git";
import { gitService } from "../services/GitService";

export function useGit(projectId: string | undefined | null) {
    const [branches, setBranches] = useState<GitBranch[]>([]);
    const [commits, setCommits] = useState<GitCommit[]>([]);
    const [activeBranch, setActiveBranch] = useState<string | null>(null);
    const [loadingBranches, setLoadingBranches] = useState<boolean>(true);
    const [loadingCommits, setLoadingCommits] = useState<boolean>(true);
    const [errorBranches, setErrorBranches] = useState<string | null>(null);
    const [errorCommits, setErrorCommits] = useState<string | null>(null);

    const fetchBranches = useCallback(async () => {
        if (!projectId) return;
        setLoadingBranches(true);
        setErrorBranches(null);
        try {
            const data = await gitService.getBranches(projectId);
            setBranches(data);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch branches";
            setErrorBranches(message);
        } finally {
            setLoadingBranches(false);
        }
    }, [projectId]);

    const fetchActiveBranch = useCallback(async () => {
        if (!projectId) return;
        try {
            const { branch } = await gitService.getActiveBranch(projectId);
            setActiveBranch(branch);
        } catch (err) {
            console.error("Failed to fetch active branch", err);
        }
    }, [projectId]);

    const fetchCommits = useCallback(async (limit: number = 20) => {
        if (!projectId) return;
        setLoadingCommits(true);
        setErrorCommits(null);
        try {
            const data = await gitService.getCommits(projectId, limit);
            setCommits(data);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch commits";
            setErrorCommits(message);
        } finally {
            setLoadingCommits(false);
        }
    }, [projectId]);

    useEffect(() => {
        if (projectId) {
            fetchBranches();
            fetchCommits();
            fetchActiveBranch();
        } else {
            setLoadingBranches(false);
            setLoadingCommits(false);
        }
    }, [projectId, fetchBranches, fetchCommits, fetchActiveBranch]);

    return {
        branches,
        commits,
        activeBranch,
        loadingBranches,
        loadingCommits,
        errorBranches,
        errorCommits,
        refetchBranches: fetchBranches,
        refetchCommits: fetchCommits
    };
}
