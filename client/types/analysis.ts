
export type LanguagesMap = Record<string, number>;
export type FrameworksMap = Record<string, number>;

export interface AnalysisData {
    languages: LanguagesMap;
    frameworks: FrameworksMap;
}
