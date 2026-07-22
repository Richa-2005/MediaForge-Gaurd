import type { AnalysisResult, UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function reportOwner(results: AnalysisResult[]) {
  return results.find((result) => result.agent === "supervisor" && (result.report || result.report_markdown || result.explanation_status !== "pending"))
    ?? results.find((result) => result.report || result.report_markdown || result.explanation_status !== "pending");
}

export function ReportGenerationState({ summary }: { summary: UploadSummary }) {
  const owner = reportOwner(summary.analysis_results);
  const status = owner?.explanation_status ?? "pending";
  const message = status === "completed"
    ? "A structured investigation report is available on the primary analysis record."
    : status === "failed"
      ? "Report generation did not complete. Available analysis results can still be reviewed."
      : "A structured report is generated after an available primary analysis result is selected.";

  return (
    <section className="report-generation scroll-reveal" aria-labelledby="report-generation-title">
      <div><p className="eyebrow">Structured report</p><h2 id="report-generation-title">The final investigation record.</h2><p>{message}</p></div>
      <div className="report-generation__action"><StatusBadge status={status} /><a className="button button--primary" href={status === "completed" ? `/results?uploadId=${summary.upload.id}` : `/dashboard?uploadId=${summary.upload.id}`}>{status === "completed" ? "Review report" : "Open dashboard"}</a></div>
    </section>
  );
}
