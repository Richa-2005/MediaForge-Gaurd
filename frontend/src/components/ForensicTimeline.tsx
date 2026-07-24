import type { ProcessingStep, UploadSummary } from "../types/dashboard";
import { formatTime } from "../utils/dateTime";
import { StatusBadge } from "./StatusBadge";

function formatDuration(duration: number | null) {
  if (duration === null) return "Duration unavailable";
  return duration < 1000 ? `${duration} ms` : `${(duration / 1000).toFixed(1)} sec`;
}

function TimelineStep({ step }: { step: ProcessingStep }) {
  return (
    <article className={`forensic-step forensic-step--${step.status}`}>
      <span className="forensic-step__node" />
      <div>
        <div className="forensic-step__top">
          <h3>{step.step_name}</h3>
          <StatusBadge status={step.status} />
        </div>
        <p>{formatDuration(step.duration_ms)}{step.started_at ? ` · Started ${formatTime(step.started_at)}` : ""}</p>
        {step.error_message && <p className="forensic-step__error">{step.error_message}</p>}
      </div>
    </article>
  );
}

export function ForensicTimeline({ summary }: { summary: UploadSummary }) {
  return (
    <section className="forensic-timeline scroll-reveal" aria-labelledby="forensic-timeline-title">
      <div className="section-heading-row">
        <div>
          <p className="eyebrow">Forensic timeline</p>
          <h2 id="forensic-timeline-title">Processing path and agent activity.</h2>
        </div>
        <span>{summary.processing_steps.length} recorded step{summary.processing_steps.length === 1 ? "" : "s"}</span>
      </div>
      {summary.processing_steps.length > 0
        ? <div className="forensic-timeline__track">{summary.processing_steps.map((step) => <TimelineStep key={step.id} step={step} />)}</div>
        : <p className="dashboard-empty">No timeline steps were recorded for this investigation.</p>}
      {summary.analysis_results.length > 0 && <div className="forensic-timeline__agents"><span>Agent outputs</span>{summary.analysis_results.map((result) => <article key={result.id}><strong>{result.agent}</strong><StatusBadge status={result.label} /><p>{Math.round(result.confidence * 100)}% confidence · {result.evidence?.length ?? 0} evidence item{(result.evidence?.length ?? 0) === 1 ? "" : "s"}</p></article>)}</div>}
    </section>
  );
}
