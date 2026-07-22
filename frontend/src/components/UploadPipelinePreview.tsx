import type { UploadStatus } from "../types/upload";

type UploadPipelinePreviewProps = {
  hasSelection: boolean;
  state: "idle" | "uploading" | "accepted" | "invalid" | "started" | "error";
  uploadStatus?: UploadStatus;
};

const stages = [
  "Media intake",
  "Media routing",
  "Specialized analysis",
  "Evidence collection",
  "LangGraph report workflow",
];

function currentStage(state: UploadPipelinePreviewProps["state"], uploadStatus?: UploadStatus) {
  if (state === "idle" || state === "invalid" || state === "error") return -1;
  if (state === "accepted" || state === "uploading") return 0;
  if (uploadStatus === "queued") return 1;
  if (uploadStatus === "processing") return 2;
  if (uploadStatus === "completed") return stages.length - 1;
  return 1;
}

export function UploadPipelinePreview({ hasSelection, state, uploadStatus }: UploadPipelinePreviewProps) {
  const active = currentStage(state, uploadStatus);
  const statusText = uploadStatus === "completed"
    ? "Processing completed. Results are ready to review."
    : uploadStatus === "failed"
      ? "Processing could not be completed."
      : state === "uploading"
        ? "Uploading media to the investigation service."
        : state === "started"
          ? "Submission accepted. Processing status updates as the service advances."
          : hasSelection
            ? "Media is ready to enter the verification workflow."
            : "Select media to preview its investigation path.";

  return (
    <section className="upload-pipeline" aria-labelledby="upload-pipeline-title">
      <div className="upload-pipeline__header">
        <p className="eyebrow">Investigation path</p>
        <h2 id="upload-pipeline-title">From intake to structured review.</h2>
      </div>
      <div className="upload-pipeline__stages" aria-label="Media analysis pipeline">
        {stages.map((stage, index) => {
          const completed = active === stages.length - 1 || index < active;
          const activeStage = index === active && active !== stages.length - 1;
          return (
            <div className={`upload-pipeline__stage ${completed ? "upload-pipeline__stage--complete" : ""} ${activeStage ? "upload-pipeline__stage--active" : ""}`} key={stage}>
              <span className="upload-pipeline__node" aria-hidden="true">{String(index + 1).padStart(2, "0")}</span>
              <span>{stage}</span>
            </div>
          );
        })}
      </div>
      <p className="upload-pipeline__status" role="status">{statusText}</p>
    </section>
  );
}
