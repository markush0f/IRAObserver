
import { useState, useEffect, useCallback } from "react";
import { LanguagesMap, FrameworksMap, Endpoint } from "../types/analysis";
import { analysisService } from "../services/AnalysisService";

export function useAnalysis(projectId: string | undefined | null) {
    const [languages, setLanguages] = useState<LanguagesMap>({});
    const [frameworks, setFrameworks] = useState<FrameworksMap>({});
    const [infrastructure, setInfrastructure] = useState<string[]>([]);
    const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        if (!projectId) return;
        setLoading(true);
        setError(null);
        try {
            const [langsData, frameworksData, infraData, endpointsData] = await Promise.all([
                analysisService.getLanguages(projectId),
                analysisService.getFrameworks(projectId),
                analysisService.getInfrastructure(projectId),
                analysisService.getEndpoints(projectId)
            ]);
            setLanguages(langsData.languages);
            setFrameworks(frameworksData.frameworks);
            setInfrastructure(infraData.components);
            setEndpoints(endpointsData.endpoints);
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

    return { languages, frameworks, infrastructure, endpoints, loading, error, refetch: fetchData };
}
