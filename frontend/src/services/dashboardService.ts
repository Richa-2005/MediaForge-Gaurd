import type { UploadSummary } from "../types/dashboard";
import type { UploadRecord } from "../types/upload";

const apiBase = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`);
  const payload: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = typeof payload === "object" && payload !== null && "detail" in payload
      ? String(payload.detail)
      : "The investigation data could not be loaded.";
    throw new Error(detail);
  }

  return payload as T;
}

export function getUploadSummary(uploadId: number) {
  return request<UploadSummary>(`/api/v1/dashboard/uploads/${uploadId}/summary`);
}

export function getRecentInvestigations(limit = 5) {
  return request<UploadRecord[]>(`/api/v1/dashboard/uploads/recent?limit=${limit}`);
}
