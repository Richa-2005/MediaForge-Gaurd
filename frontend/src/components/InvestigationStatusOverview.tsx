import type { UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function score(value: number | undefined) {
  return value === undefined ? "Not available" : `${Math.round(value * 100)}%`;
}

export function InvestigationStatusOverview({ summary }: { summary: UploadSummary }) {
  const primary = summary.analysis_results.find((result) => result.agent === "supervisor") ?? summary.analysis_results.find((result) => result.report) ?? summary.analysis_results[0];
  const totalSteps = summary.processing_steps.length;
  const completeSteps = summary.processing_steps.filter((step) => step.status === "completed" || step.status === "skipped").length;
  const progress = totalSteps ? `${completeSteps} of ${totalSteps} recorded steps complete` : "No processing steps recorded yet";

  return (
    <section className="status-overview scroll-reveal" aria-labelledby="status-overview-title">
      <div className="status-overview__heading"><p className="eyebrow">Analysis status</p><h2 id="status-overview-title">Investigation overview.</h2></div>
      <div className="status-overview__grid">
        <article><span>Processing</span><StatusBadge status={summary.processing_run?.status ?? summary.upload.status} /><p>{progress}</p></article>
        <article><span>Assessment</span>{primary ? <StatusBadge status={primary.label} /> : <strong>Awaiting analysis</strong>}<p>{primary ? primary.explanation ?? "No explanation supplied." : "No analysis result is available yet."}</p></article>
        <article><span>Confidence</span><strong>{score(primary?.confidence)}</strong><p>{primary ? "Provided by the available primary analysis result." : "Confidence is shown when analysis is available."}</p></article>
        <article><span>Risk score</span><strong>{score(primary?.risk_score)}</strong><p>{primary ? "Risk score from the available primary analysis result." : "Risk scoring is not available yet."}</p></article>
      </div>
    </section>
  );
}
