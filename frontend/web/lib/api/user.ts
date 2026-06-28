// lib/api/user.ts
import { apiClient } from "./client";

export type UserProfile = {
  id: string;
  email: string;
  full_name?: string;
  occupation?: string;
  location?: string;
  created_at: string;
};

export async function createUser(data: {
  email: string;
  full_name?: string;
}): Promise<UserProfile> {
  return apiClient.post<UserProfile>("/user/", data);
}

export async function getUser(id: string): Promise<UserProfile> {
  return apiClient.get<UserProfile>(`/user/${id}`);
}

export async function updateProfile(
  id: string,
  data: Partial<Pick<UserProfile, "full_name" | "occupation" | "location">>
): Promise<UserProfile> {
  return apiClient.patch<UserProfile>(`/user/${id}`, data);
}
