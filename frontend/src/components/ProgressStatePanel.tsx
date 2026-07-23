import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult, isReportGenerating, isReportFailed } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";
import { ProcessingSketch } from "./InvestigationMotionIllustrations";

type ProgressMode = "initializing" | "processing" | "active" | "completed" | "failed";

function progressMode(summary: UploadSummary): ProgressMode {
  if (summary.upload.status === "failed" || summary.processing_run?.status === "failed") return "failed";
  if (isReportGenerating(summary)) return "active";
  if (summary.upload.status === "completed") return "completed";
  if (summary.analysis_results.length > 0) return "active";
  if (summary.upload.status === "processing") return "processing";
  return "initializing";
}

const copy: Record<ProgressMode, { title: string; description: string }> = {
  initializing: { title: "Initializing the investigation.", description: "The service has received the submission and is preparing its processing run." },
  processing: { title: "Preparing media for analysis.", description: "The recorded preprocessing step is progressing before available specialist results are stored." },
  active: { title: "Analysis results are being assembled.", description: "Available analysis records are being retained with their evidence and assessment fields." },
  completed: { title: "The investigation is complete.", description: "The available analysis record can now be reviewed in the investigation dashboard." },
  failed: { title: "The investigation could not be completed.", description: "Review the recorded processing step for any available failure detail." },
};

export function ProgressStatePanel({ summary }: { summary: UploadSummary }) {
  const mode = progressMode(summary);
  const currentStep = summary.processing_steps.find((step) => step.status === "running")
    ?? summary.processing_steps.find((step) => step.status === "pending")
    ?? summary.processing_steps.at(-1);

  const isGenerating = isReportGenerating(summary);
  const isFailed = isReportFailed(summary);

  let title = copy[mode].title;
  let description = copy[mode].description;

  if (isGenerating) {
    title = "Generating investigation report...";
    description = "Preparing final structured assessment and finalising evidence summary.";
  } else if (isFailed) {
    title = "Structured report unavailable.";
    description = "Core forensic analysis completed successfully, but the final structured report is unavailable.";
  }

  return (
    <section className={`progress-state progress-state--${mode} scroll-reveal`} aria-labelledby="progress-state-title">
      <div className="progress-state__signal" aria-hidden="true"><ProcessingSketch mediaType={summary.upload.media_type} /><span /><span /><span /></div>
      <div className="progress-state__content">
        <p className="eyebrow">Investigation status</p>
        <h2 id="progress-state-title">{title}</h2>
        <p>{description}</p>
      </div>
      <div className="progress-state__meta">
        <StatusBadge status={summary.upload.status} />
        {currentStep && <span>Recorded stage: <strong>{currentStep.step_name}</strong></span>}
      </div>
    </section>
  );
}
