// lib/api/jobs.ts
import { apiClient } from "./client";

export type JobMatch = {
  id: string;
  title: string;
  company: string;
  match_score: number;
  location?: string;
  posted_at: string;
};

export type JobDetail = JobMatch & {
  description: string;
  requirements: string[];
};

export async function getMatches(): Promise<JobMatch[]> {
  return apiClient.get<JobMatch[]>("/jobs/matches");
}

export async function getJobDetail(id: string): Promise<JobDetail> {
  return apiClient.get<JobDetail>(`/jobs/${id}`);
}

export async function generateResume(jobId: string): Promise<{ resume_url: string }> {
  return apiClient.post<{ resume_url: string }>(`/jobs/${jobId}/resume`);
}
