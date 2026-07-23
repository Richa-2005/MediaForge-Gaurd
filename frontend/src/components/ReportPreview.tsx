import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult, isReportGenerating } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";

function MarkdownFallback({ markdown }: { markdown: string }) {
  return (
    <div className="report-preview__markdown">
      {markdown.split(/\n{2,}/).map((block) => (
        <p key={block}>{block}</p>
      ))}
    </div>
  );
}

export function ReportPreview({ summary }: { summary: UploadSummary }) {
  const owner = getPrimaryResult(summary);
  const report = owner?.report;
  const assessment = report?.verdict ?? (owner ? { label: owner.label, confidence: owner.confidence } : null);
  const findings = report?.key_findings ?? [];
  const hasStructuredDetail = Boolean(
    report?.agent_analyses?.length
    || report?.limitations
    || report?.recommendation
    || report?.technical_notes
  );

  const isGenerating = isReportGenerating(summary);
  const summaryText = isGenerating
    ? "Generating investigation report..."
    : (report?.executive_summary ?? report?.summary ?? owner?.summary ?? "The report content is not available yet.");

  return (
    <section className="report-preview scroll-reveal" aria-labelledby="report-preview-title">
      <div className="report-preview__header"><div><p className="eyebrow">Final report</p><h2 id="report-preview-title">Structured investigation report.</h2></div>{owner && <StatusBadge status={owner.explanation_status} />}</div>
      {!owner && <p className="dashboard-empty">A report is available only after an analysis result is created and selected for report generation.</p>}
      {owner && <div className="report-preview__surface"><div className="report-preview__assessment"><span>Overall assessment</span>{assessment ? <><strong>{assessment.label}</strong><p>{Math.round(assessment.confidence * 100)}% confidence</p></> : <p>No overall assessment is available yet.</p>}</div><div className="report-preview__summary"><h3>{report?.title ?? "Investigation summary"}</h3><p>{summaryText}</p></div>{findings.length > 0 && <div className="report-preview__findings"><span>Key findings</span><ul>{findings.map((finding) => <li key={finding}>{finding}</li>)}</ul></div>}{report?.agent_analyses && report.agent_analyses.length > 0 && <div className="report-preview__agents"><span>Agent analyses</span>{report.agent_analyses.map((analysis) => <article key={`${analysis.agent}-${analysis.title}`}><h3>{analysis.title || analysis.agent}</h3><p>{analysis.analysis}</p>{analysis.key_observations.length > 0 && <ul>{analysis.key_observations.map((observation) => <li key={observation}>{observation}</li>)}</ul>}</article>)}</div>}{report?.limitations && <div className="report-preview__limitations"><span>Limitations</span><p>{report.limitations}</p></div>}{report?.recommendation && <div className="report-preview__recommendation"><span>Recommended action</span><p>{report.recommendation}</p></div>}{report?.technical_notes && <div className="report-preview__technical"><span>Technical notes</span><p>{report.technical_notes}</p></div>}{!hasStructuredDetail && owner.report_markdown && <MarkdownFallback markdown={owner.report_markdown} />}</div>}
    </section>
  );
}
