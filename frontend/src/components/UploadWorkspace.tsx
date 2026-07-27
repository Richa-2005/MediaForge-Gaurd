import { ChangeEvent, DragEvent, FormEvent, useEffect, useRef, useState } from "react";
import { getUploadStatus, submitFile, submitMediaUrl } from "../services/uploadService";
import { getUploadSummary } from "../services/dashboardService";
import type { UploadSummary } from "../types/dashboard";
import type { UploadStatus } from "../types/upload";
import { isInvestigationFinished } from "../utils/investigation";
import { Icon } from "./Icon";
import { MediaPassportIllustration } from "./MediaPassportIllustration";
import { UploadPipelinePreview } from "./UploadPipelinePreview";

type IntakeState = "idle" | "uploading" | "accepted" | "invalid" | "started" | "error";

const baseSupportedExtensions = ["jpg", "jpeg", "png", "webp", "mp4", "mp3", "wav", "txt"];
const mediaExtensionGroups = {
  video: ["mp4"],
  audio: ["mp3", "wav"],
  image: ["jpg", "jpeg", "png", "webp"],
  text: ["txt"],
};
const disabledExtensions = new Set(
  String(import.meta.env.VITE_DISABLED_EXTENSIONS ?? "")
    .split(",")
    .map((extension) => extension.trim().toLowerCase().replace(/^\./, ""))
    .filter((extension: string) => Boolean(extension)),
);
const supportedExtensions = baseSupportedExtensions.filter((extension) => !disabledExtensions.has(extension));
const acceptExtensions = supportedExtensions.map((extension) => `.${extension}`).join(",");
const maxSizeMb = Number(import.meta.env.VITE_MAX_UPLOAD_SIZE_MB ?? 50);
const maxBytes = Number.isFinite(maxSizeMb) && maxSizeMb > 0 ? maxSizeMb * 1024 * 1024 : 50 * 1024 * 1024;
const supportedDescription = [
  supportedExtensions.some((extension) => mediaExtensionGroups.image.includes(extension)) ? "images" : null,
  supportedExtensions.some((extension) => mediaExtensionGroups.video.includes(extension)) ? "videos" : null,
  supportedExtensions.some((extension) => mediaExtensionGroups.audio.includes(extension)) ? "audio files" : null,
  supportedExtensions.some((extension) => mediaExtensionGroups.text.includes(extension)) ? "plain-text documents" : null,
].filter(Boolean).join(", ");

function formatBytes(size: number) {
  return `${(size / 1024 / 1024).toFixed(size >= 10 * 1024 * 1024 ? 0 : 1)} MiB`;
}

function validateFile(file: File) {
  const extension = file.name.split(".").pop()?.toLowerCase();
  if (!extension || !supportedExtensions.includes(extension)) return `This file type is not supported in this deployment. Choose ${supportedDescription || "a supported file"}.`;
  if (file.size > maxBytes) return `This file exceeds the ${formatBytes(maxBytes)} submission limit.`;
  return null;
}

export function UploadWorkspace() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [url, setUrl] = useState("");
  const [dragging, setDragging] = useState(false);
  const [intakeState, setIntakeState] = useState<IntakeState>("idle");
  const [message, setMessage] = useState<string | null>(null);
  const [uploadId, setUploadId] = useState<number | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus | undefined>();
  const [summary, setSummary] = useState<UploadSummary | null>(null);

  useEffect(() => {
    if (!uploadId || (summary && isInvestigationFinished(summary))) return;
    const interval = window.setInterval(() => {
      getUploadSummary(uploadId)
        .then((result) => {
          setSummary(result);
          setUploadStatus(result.upload.status);
        })
        .catch(() => window.clearInterval(interval));
    }, 4000);
    return () => window.clearInterval(interval);
  }, [uploadId, summary]);

  const selectFile = (file: File) => {
    const validationError = validateFile(file);
    setUploadId(null);
    setUploadStatus(undefined);
    if (validationError) {
      setSelectedFile(null);
      setIntakeState("invalid");
      setMessage(validationError);
      return;
    }
    setSelectedFile(file);
    setIntakeState("accepted");
    setMessage(null);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const [file] = Array.from(event.target.files ?? []);
    if (file) selectFile(file);
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    const [file] = Array.from(event.dataTransfer.files);
    if (file) selectFile(file);
  };

  const beginSubmission = async (submission: Promise<{ upload_id: number; status: UploadStatus; is_duplication: boolean; message: string }>) => {
    setIntakeState("uploading");
    setMessage(null);
    try {
      const response = await submission;
      setUploadId(response.upload_id);
      setUploadStatus(response.status);
      setIntakeState("started");
      setMessage(response.is_duplication ? "An existing submission was found. Its current investigation status is shown below." : response.message);
      getUploadSummary(response.upload_id)
        .then((result) => {
          setSummary(result);
          setUploadStatus(result.upload.status);
        })
        .catch(() => undefined);
    } catch (error) {
      setIntakeState("error");
      setMessage(error instanceof Error ? error.message : "The media could not be submitted.");
    }
  };

  const handleFileSubmit = () => {
    if (selectedFile) void beginSubmission(submitFile(selectedFile));
  };

  const handleUrlSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!url.trim()) {
      setIntakeState("invalid");
      setMessage("Enter a public HTTP or HTTPS media URL.");
      return;
    }
    setSelectedFile(null);
    void beginSubmission(submitMediaUrl(url.trim()));
  };

  const reset = () => {
    setSelectedFile(null);
    setUrl("");
    setUploadId(null);
    setUploadStatus(undefined);
    setSummary(null);
    setIntakeState("idle");
    setMessage(null);
    if (fileInput.current) fileInput.current.value = "";
  };

  const processingComplete = isInvestigationFinished(summary);
  const processingFailed = summary ? (summary.upload.status === "failed" || summary.processing_run?.status === "failed") : (uploadStatus === "failed");
  const passportMode = intakeState === "uploading" || intakeState === "started"
    ? "processing"
    : selectedFile || url.trim()
      ? "ready"
      : "idle";

  return (
    <div className="upload-workspace">
      <div className="upload-workspace__intro">
        <p className="eyebrow">New investigation</p>
        <h1>Submit media for a closer look.</h1>
        <p>Choose a supported file or a public media URL. The service validates the submission, queues its investigation, and retains the available review record.</p>
      </div>

      <section className="upload-intake" aria-labelledby="upload-intake-title">
        <div className="upload-intake__heading">
          <span className="upload-intake__marker" aria-hidden="true" />
          <h2 id="upload-intake-title">Media intake</h2>
        </div>

        <div
          className={`dropzone ${dragging ? "dropzone--dragging" : ""} ${intakeState === "invalid" || intakeState === "error" ? "dropzone--invalid" : ""} ${selectedFile ? "dropzone--accepted" : ""}`}
          onDragEnter={(event) => { event.preventDefault(); setDragging(true); }}
          onDragOver={(event) => event.preventDefault()}
          onDragLeave={(event) => { event.preventDefault(); setDragging(false); }}
          onDrop={handleDrop}
        >
          <input ref={fileInput} id="media-file" className="visually-hidden" type="file" accept={acceptExtensions} onChange={handleFileChange} />
          <MediaPassportIllustration mode={passportMode} />
          {!selectedFile && intakeState !== "uploading" && intakeState !== "started" && (
            <div className="dropzone__idle">
              <span className="dropzone__illustration" aria-hidden="true"><Icon name="image" size={32} /><Icon name="video" size={26} /><Icon name="audio" size={26} /><Icon name="text" size={26} /></span>
              <h3>Bring media into the investigation.</h3>
              <p>Drag and drop one supported file here, or browse from your device.</p>
              <button className="button button--primary" type="button" onClick={() => fileInput.current?.click()}>Browse files <Icon name="arrow" size={16} /></button>
            </div>
          )}

          {selectedFile && intakeState !== "uploading" && intakeState !== "started" && (
            <div className="dropzone__accepted">
              <span className="dropzone__file-icon" aria-hidden="true"><Icon name="text" size={22} /></span>
              <div><p className="dropzone__file-name">{selectedFile.name}</p><p className="dropzone__file-meta">{formatBytes(selectedFile.size)} · Ready for submission</p></div>
              <div className="dropzone__file-actions"><button className="button button--primary" type="button" onClick={handleFileSubmit}>Start analysis <Icon name="arrow" size={16} /></button><button className="quiet-button" type="button" onClick={reset}>Remove</button></div>
            </div>
          )}

          {intakeState === "uploading" && <div className="dropzone__progress" role="status"><span className="indeterminate-line" aria-hidden="true" /><h3>Submitting media</h3><p>The service is validating and storing your submission.</p></div>}

          {intakeState === "started" && (
            <div className="dropzone__started" role="status">
              <span className="dropzone__started-mark" aria-hidden="true">✓</span>
              <div><h3>{processingComplete ? "Analysis completed" : processingFailed ? "Analysis stopped" : "Processing started"}</h3><p>{message}</p></div>
              <a className="button button--primary" href={processingComplete ? `/results?uploadId=${uploadId}` : `/progress?uploadId=${uploadId}`}>{processingComplete ? "View results" : "View progress"} <Icon name="arrow" size={16} /></a>
            </div>
          )}

          {(intakeState === "invalid" || intakeState === "error") && <div className="dropzone__feedback" role="alert"><p>{message}</p><button className="quiet-button" type="button" onClick={reset}>Try another file</button></div>}
        </div>

        <div className="upload-intake__divider"><span>or</span></div>
        <form className="url-intake" onSubmit={handleUrlSubmit}>
          <label htmlFor="media-url">Submit a public media URL</label>
          <div><input id="media-url" type="url" value={url} onChange={(event) => setUrl(event.target.value)} placeholder="https://example.com/media" /><button className="quiet-button" type="submit" disabled={intakeState === "uploading"}>Analyze URL <Icon name="arrow" size={15} /></button></div>
        </form>
      </section>

      <UploadPipelinePreview hasSelection={Boolean(selectedFile || url)} state={intakeState} uploadStatus={uploadStatus} />
    </div>
  );
}
