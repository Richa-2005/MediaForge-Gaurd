import type { UploadSummary, AnalysisResult } from "../types/dashboard";

export function getPrimaryResult(summary: UploadSummary | null): AnalysisResult | undefined {
  if (!summary || !summary.analysis_results || !summary.analysis_results.length) return undefined;

  // 1. Explicit primary result / primary_analysis_id, if exposed
  const explicitId = (summary as any).primary_analysis_id
    ?? (summary.upload as any).primary_analysis_id
    ?? (summary.processing_run as any).primary_analysis_id;
  if (typeof explicitId === "number") {
    const explicitResult = summary.analysis_results.find((r) => r.id === explicitId);
    if (explicitResult) return explicitResult;
  }

  // 2. Supervisor result
  const supervisor = summary.analysis_results.find((r) => r.agent === "supervisor");
  if (supervisor) return supervisor;

  // 3. Result containing the completed report
  const reportOwner = summary.analysis_results.find((r) => r.report || r.report_markdown || r.summary);
  if (reportOwner) return reportOwner;

  // 4. First available analysis result as a defensive fallback
  return summary.analysis_results[0];
}

export function isInvestigationFinished(summary: UploadSummary | null): boolean {
  if (!summary) return false;
  if (summary.upload.status === "failed" || summary.processing_run?.status === "failed") {
    return true;
  }
  if (summary.upload.status === "completed") {
    const primaryResult = getPrimaryResult(summary);
    if (!primaryResult) return true; // defensive fallback if no results exist
    const explanationStatus = primaryResult.explanation_status;
    return explanationStatus === "completed" || explanationStatus === "failed";
  }
  return false;
}

export function isReportGenerating(summary: UploadSummary | null): boolean {
  if (!summary) return false;
  if (summary.upload.status !== "completed") return false;
  if (!summary.analysis_results || summary.analysis_results.length === 0) return false;

  const primaryResult = getPrimaryResult(summary);
  if (!primaryResult) return false;

  const explanationStatus = primaryResult.explanation_status;
  // Report status is neither completed nor failed -> generating
  return explanationStatus !== "completed" && explanationStatus !== "failed";
}

export function isReportFailed(summary: UploadSummary | null): boolean {
  if (!summary) return false;
  if (summary.upload.status !== "completed") return false;
  const primaryResult = getPrimaryResult(summary);
  return primaryResult?.explanation_status === "failed";
}
