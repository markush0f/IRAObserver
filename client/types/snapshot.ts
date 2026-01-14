
export type Snapshot = {
    id: string;
    project_id: string;
    commit_hash: string | null;
    created_at: string;
    summary_json?: any;
};

export type SnapshotResponse = {
    items: Snapshot[];
    total: number;
    limit: number;
    offset: number;
};
