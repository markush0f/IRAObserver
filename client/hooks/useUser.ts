
import { useState, useEffect, useCallback } from "react";
import { User } from "../types/user";
import { userService } from "../services/UserService";

export function useUser() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchUser = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await userService.getProfile();
            setUser(data);
        } catch (err: unknown) {
            if (err instanceof Error && err.message.includes("401")) {
                setUser(null);
            } else {
                const message = err instanceof Error ? err.message : "Failed to fetch user";
                setError(message);
            }
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUser();
    }, [fetchUser]);

    return { user, loading, error, refetch: fetchUser };
}
