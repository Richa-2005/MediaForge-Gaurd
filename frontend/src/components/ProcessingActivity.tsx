import type { ProcessingStep, UploadSummary } from "../types/dashboard";
import { formatTime } from "../utils/dateTime";
import { describeStep, formatStepName } from "../utils/processingSteps";
import { StatusBadge } from "./StatusBadge";

function formatDuration(duration: number | null) {
  if (duration === null) return null;
  return duration < 1000 ? `${duration} ms` : `${(duration / 1000).toFixed(1)} sec`;
}

function ActivityStep({ step }: { step: ProcessingStep }) {
  return (
    <article className="activity-step">
      <div className="activity-step__title"><h3>{formatStepName(step.step_name)}</h3><StatusBadge status={step.status} /></div>
      <div className="activity-step__details">
        {formatDuration(step.duration_ms) && <span>{formatDuration(step.duration_ms)}</span>}
        {step.started_at && <span>Started {formatTime(step.started_at)}</span>}
      </div>
      <p>{describeStep(step.step_name)}</p>
      {step.error_message && <p className="activity-step__error">{step.error_message}</p>}
    </article>
  );
}

export function ProcessingActivity({ summary }: { summary: UploadSummary }) {
  return (
    <section className="processing-activity scroll-reveal" aria-labelledby="processing-activity-title">
      <div className="processing-activity__heading"><p className="eyebrow">Recorded activity</p><h2 id="processing-activity-title">The processing record.</h2></div>
      {summary.processing_steps.length > 0 ? <div className="processing-activity__list">{summary.processing_steps.map((step) => <ActivityStep key={step.id} step={step} />)}</div> : <p className="dashboard-empty">No processing steps have been recorded for this investigation yet.</p>}
    </section>
  );
}
