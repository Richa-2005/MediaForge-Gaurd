import type { UploadRecord, UploadStatusResponse, UploadSubmissionResponse } from "../types/upload";

const apiBase = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, init);
  const payload: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = typeof payload === "object" && payload !== null && "detail" in payload
      ? String(payload.detail)
      : "The request could not be completed.";
    throw new Error(detail);
  }

  return payload as T;
}

export function submitFile(file: File) {
  const formData = new FormData();
  formData.append("uploaded_file", file);
  return request<UploadSubmissionResponse>("/api/v1/uploads", {
    method: "POST",
    body: formData,
  });
}

export function submitMediaUrl(url: string) {
  return request<UploadSubmissionResponse>("/api/v1/uploads/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
}

export function getUploadStatus(uploadId: number) {
  return request<UploadStatusResponse>(`/api/v1/uploads/${uploadId}`);
}

export function getRecentUploads(limit = 5) {
  return request<UploadRecord[]>(`/api/v1/dashboard/uploads/recent?limit=${limit}`);
}
