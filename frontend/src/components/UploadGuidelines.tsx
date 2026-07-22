export function UploadGuidelines() {
  return (
    <aside className="upload-guidelines" aria-labelledby="guidelines-title">
      <p className="eyebrow">Before you submit</p>
      <h2 id="guidelines-title">Media intake, clearly defined.</h2>
      <dl>
        <div>
          <dt>Supported files</dt>
          <dd>JPEG, PNG, WebP, MP4, MP3, WAV, and plain-text documents.</dd>
        </div>
        <div>
          <dt>Maximum size</dt>
          <dd>50 MiB per submission.</dd>
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
