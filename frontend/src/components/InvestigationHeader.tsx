import type { UploadSummary } from "../types/dashboard";
import { formatTimestamp } from "../utils/dateTime";
import { isInvestigationFinished } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";

export function InvestigationHeader({ summary }: { summary: UploadSummary }) {
  const step = summary.processing_steps.find((item) => item.status === "running")
    ?? summary.processing_steps.find((item) => item.status === "pending")
    ?? summary.processing_steps.at(-1);

  return (
    <header className="investigation-header scroll-reveal">
      <div className="investigation-header__title">
        <p className="eyebrow">Submission #{summary.upload.id}</p>
        <h1>{summary.upload.original_filename}</h1>
        <div className="investigation-header__meta">
          <span>{summary.upload.media_type}</span>
          <span>{formatTimestamp(summary.upload.created_at)}</span>
          {step && <span>Current stage: {step.step_name}</span>}
        </div>
      </div>
      <div className="investigation-header__status">
        <StatusBadge status={summary.upload.status} />
        {summary.processing_run && <span className="investigation-header__run">Run {summary.processing_run.status}</span>}
        {!isInvestigationFinished(summary) && <a className="investigation-header__progress-link" href={`/progress?uploadId=${summary.upload.id}`}>Follow progress</a>}
        {isInvestigationFinished(summary) && summary.upload.status === "completed" && <a className="investigation-header__progress-link" href={`/results?uploadId=${summary.upload.id}`}>Review results</a>}
      </div>
    </header>
  );
}
