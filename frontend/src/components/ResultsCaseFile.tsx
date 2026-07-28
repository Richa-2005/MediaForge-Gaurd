import { getStoredToken } from "../services/tokenStore";
import { apiBase } from "../services/apiClient";
import type { AnalysisAgent, UploadSummary } from "../types/dashboard";
import { getPrimaryResult } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";

const agentLabels: Record<AnalysisAgent, string> = {
  text: "Text",
  vision: "Vision",
  video: "Video",
  audio: "Audio",
  factcheck: "Fact check",
  supervisor: "Supervisor",
};

function MediaPreview({ summary }: { summary: UploadSummary }) {
  const mediaType = summary.upload.media_type;
  const normalized = mediaType.toLowerCase();
  const mode = normalized.includes("image")
    ? "image"
    : normalized.includes("video")
      ? "video"
      : normalized.includes("audio")
        ? "audio"
        : normalized.includes("text")
          ? "text"
          : "media";

  const token = getStoredToken();
  const mediaUrl = `${apiBase}/api/v1/uploads/${summary.upload.id}/media${token ? `?token=${encodeURIComponent(token)}` : ""}`;

  return (
    <div className={`case-file-preview case-file-preview--${mode}`}>
      <div className="case-file-preview__scan" />
      <div className="case-file-preview__frame">
        {mode === "image" ? (
          <img src={mediaUrl} alt={`Uploaded media preview for ${summary.upload.original_filename}`} />
        ) : mode === "video" ? (
          <video src={mediaUrl} controls preload="metadata" aria-label={`Uploaded video preview for ${summary.upload.original_filename}`} />
        ) : mode === "audio" ? (
          <>
            <audio src={mediaUrl} controls aria-label={`Uploaded audio preview for ${summary.upload.original_filename}`} />
            <div className="case-file-preview__wave">{Array.from({ length: 22 }).map((_, index) => <span key={index} />)}</div>
          </>
        ) : mode === "text" ? (
          <iframe src={mediaUrl} title={`Uploaded text preview for ${summary.upload.original_filename}`} />
        ) : (
          <div className="case-file-preview__image"><span /><i /><b /></div>
        )}
      </div>
    </div>
  );
}

export function ResultsCaseFile({ summary }: { summary: UploadSummary }) {
  const primary = getPrimaryResult(summary);
  const label = primary?.report?.verdict?.label ?? primary?.label ?? "uncertain";
  const confidence = primary?.report?.verdict?.confidence ?? primary?.confidence ?? 0;
  const riskScore = primary?.risk_score ?? 0;
  const evidenceCount = summary.analysis_results.reduce((total, result) => total + (result.evidence?.length ?? 0), 0);
  const completedSteps = summary.processing_steps.filter((step) => step.status === "completed").length;
  const agentCount = summary.analysis_results.length;

  return (
    <section className={`case-file case-file--${label} scroll-reveal`} aria-labelledby="case-file-title">
      <div className="case-file__content">
        <p className="eyebrow">Forensic case file</p>
        <h2 id="case-file-title">{primary?.report?.title ?? "Investigation result overview"}</h2>
        <p>Review the submitted media, assembled evidence, timeline, specialist findings, and final report in one case record.</p>
        <div className="case-file__actions">
          <a className="text-link" href="#investigation-summary">Jump to summary <span aria-hidden="true">-&gt;</span></a>
        </div>
        <div className="case-file__agents" aria-label="Analysis agents included">
          {summary.analysis_results.map((result) => (
            <span key={result.id}>{agentLabels[result.agent]}</span>
          ))}
        </div>
      </div>
      <div className="case-file__visual">
        <MediaPreview summary={summary} />
        <div className="case-file__verdict">
          <StatusBadge status={label as "authentic" | "manipulated" | "uncertain"} />
          <strong>{Math.round(confidence * 100)}%</strong>
          <span>confidence</span>
        </div>
      </div>
      <dl className="case-file__metrics">
        <div><dt>Risk score</dt><dd>{Math.round(riskScore * 100)}%</dd></div>
        <div><dt>Evidence items</dt><dd>{evidenceCount}</dd></div>
        <div><dt>Agents returned</dt><dd>{agentCount}</dd></div>
        <div><dt>Steps completed</dt><dd>{completedSteps}/{summary.processing_steps.length || 0}</dd></div>
      </dl>
    </section>
  );
}
