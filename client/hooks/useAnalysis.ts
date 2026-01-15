
import { useState, useEffect, useCallback } from "react";
import { LanguagesMap, FrameworksMap } from "../types/analysis";
import { analysisService } from "../services/AnalysisService";

export function useAnalysis(projectId: string | undefined | null) {
    const [languages, setLanguages] = useState<LanguagesMap>({});
    const [frameworks, setFrameworks] = useState<FrameworksMap>({});
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        if (!projectId) return;
        setLoading(true);
        setError(null);
        try {
            const [langsData, frameworksData] = await Promise.all([
                analysisService.getLanguages(projectId),
                analysisService.getFrameworks(projectId)
            ]);
            setLanguages(langsData.languages);
            setFrameworks(frameworksData.frameworks);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to fetch analysis data";
            setError(message);
        } finally {
            setLoading(false);
        }
    }, [projectId]);

    useEffect(() => {
        if (projectId) {
            fetchData();
        } else {
            setLoading(false);
        }
    }, [projectId, fetchData]);

    return { languages, frameworks, loading, error, refetch: fetchData };
}
