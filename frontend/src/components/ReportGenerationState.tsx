import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";
import { ReportAssemblyIllustration } from "./InvestigationMotionIllustrations";

export function ReportGenerationState({ summary }: { summary: UploadSummary }) {
  const primaryResult = getPrimaryResult(summary);
  const status = primaryResult?.explanation_status ?? "pending";

  const message = status === "completed"
    ? "A structured investigation report is available on the primary analysis record."
    : status === "failed"
      ? "Structured report unavailable. Core forensic analysis completed successfully."
      : summary.upload.status === "completed"
        ? "Generating investigation report... Preparing final structured assessment..."
        : "A structured report is generated after an available primary analysis result is selected.";

  const canNavigate = status === "completed" || status === "failed";
  const buttonText = status === "completed"
    ? "Review report"
    : status === "failed"
      ? "Review results"
      : summary.upload.status === "completed"
        ? "Generating report..."
        : "Open dashboard";
  const buttonHref = canNavigate
    ? `/results?uploadId=${summary.upload.id}`
    : `/dashboard?uploadId=${summary.upload.id}`;

  return (
    <section className="report-generation scroll-reveal" aria-labelledby="report-generation-title">
      <ReportAssemblyIllustration />
      <div><p className="eyebrow">Structured report</p><h2 id="report-generation-title">The final investigation record.</h2><p>{message}</p></div>
      <div className="report-generation__action">
        <StatusBadge status={status} />
        {!canNavigate && summary.upload.status === "completed" ? (
          <button className="button button--primary" disabled style={{ opacity: 0.6, cursor: "not-allowed" }}>
            {buttonText}
          </button>
        ) : (
          <a className="button button--primary" href={buttonHref}>
            {buttonText}
          </a>
        )}
      </div>
    </section>
  );
}
