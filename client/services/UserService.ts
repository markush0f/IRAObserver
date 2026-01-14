
import { apiClient } from "../lib/api-client";
import { User } from "../types/user";

export class UserService {
    async getProfile(): Promise<User> {
        return apiClient.get<User>("/auth/me");
    }

    async updateProfile(data: Partial<User>): Promise<User> {
        return apiClient.put<User>("/users/me", data);
    }

    // Example of usage for auth (though Auth might be a separate service usually)
    async register(username: string, password: string): Promise<User> {
        return apiClient.post<User>("/auth/register", { username, password });
    }

    async login(username: string, password: string): Promise<{ user: User; token: string }> {
        return apiClient.post<{ user: User; token: string }>("/auth/login", { username, password });
    }
}

export const userService = new UserService();
