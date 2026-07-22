export type UploadStatus = "uploaded" | "queued" | "processing" | "completed" | "failed";

export type UploadSubmissionResponse = {
  upload_id: number;
  status: UploadStatus;
  media_type: string;
  file_path?: string;
  is_duplication: boolean;
  message: string;
};

export type UploadRecord = {
  id: number;
  status: UploadStatus;
  media_type: string;
  file_path: string;
  original_filename: string;
  stored_filename: string;
  sha256_hash: string;
  created_at: string;
};

export type UploadStatusResponse = {
  upload_id: number;
  status: UploadStatus;
  media_type: string;
  file_path: string;
  original_filename: string;
  stored_filename: string;
};
