import type { UploadSummary } from "../types/dashboard";
import { formatTimestamp } from "../utils/dateTime";
import { isInvestigationFinished } from "../utils/investigation";
import { currentStep, formatStepName } from "../utils/processingSteps";
import { StatusBadge } from "./StatusBadge";

export function InvestigationHeader({ summary }: { summary: UploadSummary }) {
  const step = currentStep(summary);
  const path = window.location.pathname;
  const showProgressLink = !isInvestigationFinished(summary) && path !== "/progress";
  const showResultsLink = isInvestigationFinished(summary) && summary.upload.status === "completed" && path !== "/results";

  return (
    <header className="investigation-header scroll-reveal">
      <div className="investigation-header__title">
        <p className="eyebrow">Submission #{summary.upload.id}</p>
        <h1>{summary.upload.original_filename}</h1>
        <div className="investigation-header__meta">
          <span>{summary.upload.media_type}</span>
          <span>{formatTimestamp(summary.upload.created_at)}</span>
          {step && <span>Current stage: {formatStepName(step.step_name)}</span>}
        </div>
      </div>
      <div className="investigation-header__status">
        <StatusBadge status={summary.upload.status} />
        {summary.processing_run && <span className="investigation-header__run">Run {summary.processing_run.status}</span>}
        {showProgressLink && <a className="investigation-header__progress-link" href={`/progress?uploadId=${summary.upload.id}`}>Follow progress</a>}
        {showResultsLink && <a className="investigation-header__progress-link" href={`/results?uploadId=${summary.upload.id}`}>Review results</a>}
      </div>
    </header>
  );
}
