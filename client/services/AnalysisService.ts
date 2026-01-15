
import { apiClient } from "../lib/api-client";
import { LanguagesMap, FrameworksMap, InfrastructureResponse, EndpointsResponse } from "../types/analysis";

export class AnalysisService {
    async getLanguages(projectId: string): Promise<{ languages: LanguagesMap }> {
        return apiClient.get<{ languages: LanguagesMap }>(`/projects/${projectId}/analysis/languages`);
    }

    async getFrameworks(projectId: string): Promise<{ frameworks: FrameworksMap }> {
        // User specified POST for frameworks
        return apiClient.post<{ frameworks: FrameworksMap }>(`/projects/${projectId}/analysis/frameworks`, {});
    }

    async getInfrastructure(projectId: string): Promise<InfrastructureResponse> {
        return apiClient.get<InfrastructureResponse>(`/projects/${projectId}/analysis/infrastructure`);
    }

    async getEndpoints(projectId: string): Promise<EndpointsResponse> {
        return apiClient.get<EndpointsResponse>(`/projects/${projectId}/analysis/endpoints`);
    }
}

export const analysisService = new AnalysisService();
