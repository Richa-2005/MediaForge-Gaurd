import type { UploadRecord, UploadStatusResponse, UploadSubmissionResponse } from "../types/upload";
import { apiRequest } from "./apiClient";

export function submitFile(file: File) {
  const formData = new FormData();
  formData.append("uploaded_file", file);
  return apiRequest<UploadSubmissionResponse>("/api/v1/uploads", {
    method: "POST",
    body: formData,
    errorMessage: "The media could not be submitted.",
  });
}

export function submitMediaUrl(url: string) {
  return apiRequest<UploadSubmissionResponse>("/api/v1/uploads/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
    errorMessage: "The media URL could not be submitted.",
  });
}

export function getUploadStatus(uploadId: number) {
  return apiRequest<UploadStatusResponse>(`/api/v1/uploads/${uploadId}`);
}

export function getRecentUploads(limit = 5) {
  return apiRequest<UploadRecord[]>(`/api/v1/dashboard/uploads/recent?limit=${limit}`);
}
