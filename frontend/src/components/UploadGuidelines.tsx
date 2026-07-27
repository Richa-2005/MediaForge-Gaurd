export function UploadGuidelines() {
  const disabled = new Set(
    String(import.meta.env.VITE_DISABLED_EXTENSIONS ?? "")
      .split(",")
      .map((extension) => extension.trim().toLowerCase().replace(/^\./, ""))
      .filter((extension: string) => Boolean(extension)),
  );
  const supported = [
    ["jpg", "JPEG"],
    ["png", "PNG"],
    ["webp", "WebP"],
    ["mp4", "MP4"],
    ["mp3", "MP3"],
    ["wav", "WAV"],
    ["txt", "plain-text documents"],
  ]
    .filter(([extension]) => !disabled.has(extension))
    .map(([, label]) => label);
  const maxSize = Number(import.meta.env.VITE_MAX_UPLOAD_SIZE_MB ?? 50);

  return (
    <aside className="upload-guidelines" aria-labelledby="guidelines-title">
      <p className="eyebrow">Before you submit</p>
      <h2 id="guidelines-title">Media intake, clearly defined.</h2>
      <dl>
        <div>
          <dt>Supported files</dt>
          <dd>{supported.join(", ")}.</dd>
        </div>
        <div>
          <dt>Maximum size</dt>
          <dd>{Number.isFinite(maxSize) && maxSize > 0 ? maxSize : 50} MiB per submission.</dd>
        </div>
        <div>
          <dt>Service validation</dt>
          <dd>Media type and file content are checked by the service before processing.</dd>
        </div>
        <div>
          <dt>Review record</dt>
          <dd>Available evidence, processing metadata, and result status remain associated with the submission.</dd>
        </div>
      </dl>
    </aside>
  );
}
