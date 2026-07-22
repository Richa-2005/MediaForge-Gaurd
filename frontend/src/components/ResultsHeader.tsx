import type { UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

function formatTimestamp(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Timestamp unavailable" : date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

export function ResultsHeader({ summary }: { summary: UploadSummary }) {
  return (
    <header className="results-header scroll-reveal">
      <div>
        <p className="eyebrow">Investigation results</p>
        <h1>{summary.upload.original_filename}</h1>
        <div className="results-header__meta"><span>{summary.upload.media_type}</span><span>Submitted {formatTimestamp(summary.upload.created_at)}</span><span>Submission #{summary.upload.id}</span></div>
      </div>
      <div className="results-header__actions"><StatusBadge status={summary.upload.status} /><a className="text-link" href={`/dashboard?uploadId=${summary.upload.id}`}>Open dashboard <span aria-hidden="true">→</span></a></div>
    </header>
  );
}
