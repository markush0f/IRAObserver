
export type LanguagesMap = Record<string, number>;
export type FrameworksMap = Record<string, number>;

export interface AnalysisData {
    languages: LanguagesMap;
    frameworks: FrameworksMap;
}

export interface InfrastructureResponse {
    components: string[];
}

export interface Endpoint {
    id: string;
    snapshot_id: string;
    http_method: string;
    path: string;
    framework: string;
    language: string;
    source_file: string;
    source_symbol: string | null;
    confidence: number;
    created_at: string;
}

export interface EndpointsResponse {
    endpoints: Endpoint[];
}
