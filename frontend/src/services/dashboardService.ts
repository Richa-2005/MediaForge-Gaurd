import type { UploadSummary } from "../types/dashboard";
import type { UploadRecord } from "../types/upload";
import { apiRequest } from "./apiClient";

export function getUploadSummary(uploadId: number) {
  return apiRequest<UploadSummary>(`/api/v1/dashboard/uploads/${uploadId}/summary`, {
    errorMessage: "The investigation data could not be loaded.",
  });
}

export function getRecentInvestigations(limit = 5) {
  return apiRequest<UploadRecord[]>(`/api/v1/dashboard/uploads/recent?limit=${limit}`, {
    errorMessage: "The investigation data could not be loaded.",
  });
}
