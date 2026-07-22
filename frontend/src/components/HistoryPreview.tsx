import type { UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function primaryResult(summary: UploadSummary) {
  return summary.analysis_results.find((result) => result.agent === "supervisor")
    ?? summary.analysis_results.find((result) => result.report || result.summary)
    ?? summary.analysis_results[0];
}

export function HistoryPreview({ summary, loading, error }: { summary: UploadSummary | null; loading: boolean; error: string | null }) {
  if (loading) return <aside className="history-preview history-preview--loading" aria-label="Loading selected investigation"><span /><span /><span /></aside>;
  if (error) return <aside className="history-preview history-preview--message"><p role="alert">{error}</p></aside>;
  if (!summary) return <aside className="history-preview history-preview--message"><p>Select a returned submission to inspect its available summary.</p></aside>;

  const result = primaryResult(summary);
  const destination = summary.upload.status === "completed" ? `/results?uploadId=${summary.upload.id}` : `/progress?uploadId=${summary.upload.id}`;
  const destinationLabel = summary.upload.status === "completed" ? "Open results" : "Follow progress";

  return (
    <aside className="history-preview" aria-labelledby="history-preview-title">
      <p className="eyebrow">Selected investigation</p>
      <h2 id="history-preview-title">{summary.upload.original_filename}</h2>
      <div className="history-preview__meta"><StatusBadge status={summary.upload.status} /><span>{summary.upload.media_type}</span><span>#{summary.upload.id}</span></div>
      {result ? <div className="history-preview__assessment"><span>Available assessment</span><StatusBadge status={result.label} /><strong>{Math.round(result.confidence * 100)}% confidence</strong><p>{result.summary ?? result.explanation ?? "No assessment summary was supplied."}</p></div> : <p className="history-preview__no-result">No analysis result is available for this submission yet.</p>}
      <a className="button button--primary" href={destination}>{destinationLabel}</a>
    </aside>
  );
}
