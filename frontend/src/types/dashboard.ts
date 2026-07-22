import type { UploadRecord, UploadStatus } from "./upload";

export type RunStatus = "running" | "completed" | "failed" | "cancelled";
export type StepStatus = "running" | "completed" | "failed" | "skipped" | "pending";
export type AnalysisAgent = "vision" | "audio" | "video" | "text" | "factcheck" | "supervisor";
export type AnalysisLabel = "authentic" | "manipulated" | "uncertain";
export type ExplanationStatus = "pending" | "completed" | "failed";

export type ProcessingRun = {
  id: number;
  upload_id: number;
  status: RunStatus;
  trigger: "upload" | "reanalysis" | "manual" | "scheduled";
  started_at: string;
  completed_at: string | null;
  created_at: string;
  duration_ms: number | null;
};

export type ProcessingStep = {
  id: number;
  processing_run_id: number;
  step_name: string;
  status: StepStatus;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  created_at: string;
  duration_ms: number | null;
};

export type Evidence = {
  method?: string;
  score?: number;
  confidence?: number;
  summary?: string;
  artifact_path?: string | null;
  metadata?: Record<string, unknown>;
};

export type AnalysisResult = {
  id: number;
  upload_id: number;
  agent: AnalysisAgent;
  label: AnalysisLabel;
  risk_score: number;
  confidence: number;
  explanation: string | null;
  evidence: Evidence[] | null;
  details: Record<string, unknown> | null;
  created_at: string;
  report: InvestigationReport | null;
  report_markdown: string | null;
  summary: string | null;
  explanation_status: ExplanationStatus;
  explanation_generated_at: string | null;
};

export type ProcessingArtifact = {
  id: number;
  upload_id: number;
  artifact_type: string;
  file_path: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
};

export type InvestigationReport = {
  title?: string;
  verdict?: { label: string; confidence: number };
  summary?: string;
  executive_summary?: string;
  agent_analyses?: Array<{ agent: string; title: string; analysis: string; key_observations: string[] }>;
  key_findings?: string[];
  limitations?: string;
  recommendation?: string;
  technical_notes?: string;
};

export type UploadSummary = {
  upload: UploadRecord;
  processing_run: ProcessingRun | null;
  processing_steps: ProcessingStep[];
  analysis_results: AnalysisResult[];
  artifacts: ProcessingArtifact[];
};

export type StatusValue = UploadStatus | RunStatus | StepStatus | ExplanationStatus | AnalysisLabel;
