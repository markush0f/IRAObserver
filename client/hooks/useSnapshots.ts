
import { useState, useEffect, useCallback } from "react";
import { Snapshot } from "../types/snapshot";
import { snapshotService } from "../services/SnapshotService";

export function useSnapshots(projectId: string | undefined | null) {
    const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
    const [total, setTotal] = useState<number>(0);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchSnapshots = useCallback(async () => {
        if (!projectId) return;

        setLoading(true);
        setError(null);
        try {
            const response = await snapshotService.getCompact(projectId);
            setSnapshots(response.items);
            setTotal(response.total);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch snapshots";
            setError(message);
        } finally {
            setLoading(false);
        }
    }, [projectId]);

    useEffect(() => {
        if (projectId) {
            fetchSnapshots();
        } else {
            setLoading(false);
        }
    }, [projectId, fetchSnapshots]);

    return { snapshots, total, loading, error, refetch: fetchSnapshots };
}
