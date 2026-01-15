
import { apiClient } from "../lib/api-client";
import { LanguagesMap, FrameworksMap } from "../types/analysis";

export class AnalysisService {
    async getLanguages(projectId: string): Promise<{ languages: LanguagesMap }> {
        return apiClient.get<{ languages: LanguagesMap }>(`/projects/${projectId}/analysis/languages`);
    }

    async getFrameworks(projectId: string): Promise<{ frameworks: FrameworksMap }> {
        // User specified POST for frameworks
        return apiClient.post<{ frameworks: FrameworksMap }>(`/projects/${projectId}/analysis/frameworks`, {});
    }
}

export const analysisService = new AnalysisService();
