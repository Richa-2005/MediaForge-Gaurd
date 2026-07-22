import type { AnalysisResult, UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function reportOwner(results: AnalysisResult[]) {
  return results.find((result) => result.agent === "supervisor" && (result.report || result.report_markdown || result.summary))
    ?? results.find((result) => result.report || result.report_markdown || result.summary || result.explanation_status !== "pending");
}

export function ReportPreview({ summary }: { summary: UploadSummary }) {
  const owner = reportOwner(summary.analysis_results);
  const report = owner?.report;
  const assessment = report?.verdict ?? (owner ? { label: owner.label, confidence: owner.confidence } : null);
  const findings = report?.key_findings ?? [];

  return (
    <section className="report-preview scroll-reveal" aria-labelledby="report-preview-title">
      <div className="report-preview__header"><div><p className="eyebrow">Final report</p><h2 id="report-preview-title">Structured investigation report.</h2></div>{owner && <StatusBadge status={owner.explanation_status} />}</div>
      {!owner && <p className="dashboard-empty">A report is available only after an analysis result is created and selected for report generation.</p>}
      {owner && <div className="report-preview__surface"><div className="report-preview__assessment"><span>Overall assessment</span>{assessment ? <><strong>{assessment.label}</strong><p>{Math.round(assessment.confidence * 100)}% confidence</p></> : <p>No overall assessment is available yet.</p>}</div><div className="report-preview__summary"><h3>{report?.title ?? "Investigation summary"}</h3><p>{report?.executive_summary ?? report?.summary ?? owner.summary ?? "The report content is not available yet."}</p></div>{findings.length > 0 && <div className="report-preview__findings"><span>Key findings</span><ul>{findings.map((finding) => <li key={finding}>{finding}</li>)}</ul></div>}{report?.recommendation && <div className="report-preview__recommendation"><span>Recommended action</span><p>{report.recommendation}</p></div>}</div>}
    </section>
  );
}
