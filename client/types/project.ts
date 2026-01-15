
export type Project = {
    id: string;
    name: string;
    description: string;
    source_type: string;
    source_ref: string;
    created_at: string;
    last_analysis_at: string | null;
};
export type MembershipUser = {
    id: string;
    display_name: string;
    role: string;
    is_active: boolean;
    created_at: string;
};

export type ProjectMember = {
    id: string;
    user: MembershipUser;
    role: string;
    created_at: string;
    revoked_at: string | null;
};
