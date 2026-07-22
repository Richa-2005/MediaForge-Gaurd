import type { AnalysisResult, UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function primaryResult(results: AnalysisResult[]) {
  return results.find((result) => result.agent === "supervisor")
    ?? results.find((result) => result.report || result.report_markdown || result.summary)
    ?? results[0];
}

export function ResultsSummaryCard({ summary }: { summary: UploadSummary }) {
  const primary = primaryResult(summary.analysis_results);
  const report = primary?.report;
  const assessment = report?.verdict ?? (primary ? { label: primary.label, confidence: primary.confidence } : null);
  const findings = report?.key_findings ?? [];

  if (!primary) {
    return <section className="results-incomplete scroll-reveal" aria-labelledby="results-incomplete-title"><div><p className="eyebrow">Investigation summary</p><h2 id="results-incomplete-title">Analysis results are not available yet.</h2><p>The submission record exists, but the backend has not returned any analysis result for it.</p></div><a className="button button--primary" href={`/progress?uploadId=${summary.upload.id}`}>Follow progress</a></section>;
  }

  return (
    <section className="results-summary scroll-reveal" aria-labelledby="results-summary-title">
      <div className="results-summary__assessment">
        <p className="eyebrow">Overall assessment</p>
        {assessment && <><StatusBadge status={assessment.label as "authentic" | "manipulated" | "uncertain"} /><h2 id="results-summary-title">{assessment.label}</h2><p>{Math.round(assessment.confidence * 100)}% confidence</p></>}
        <div className="results-summary__score"><span>Risk score</span><strong>{Math.round(primary.risk_score * 100)}%</strong></div>
      </div>
      <div className="results-summary__content">
        <p className="eyebrow">Investigation summary</p>
        <h2>{report?.title ?? "Available analysis summary"}</h2>
        <p>{report?.executive_summary ?? report?.summary ?? primary.summary ?? primary.explanation ?? "No summary was supplied."}</p>
        {findings.length > 0 && <div className="results-summary__findings"><span>Key findings</span><ul>{findings.map((finding) => <li key={finding}>{finding}</li>)}</ul></div>}
      </div>
    </section>
  );
}
