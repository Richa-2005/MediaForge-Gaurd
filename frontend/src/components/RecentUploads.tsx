import { useEffect, useState } from "react";
import { getRecentUploads } from "../services/uploadService";
import type { UploadRecord } from "../types/upload";
import { formatDate } from "../utils/dateTime";

export function RecentUploads() {
  const [uploads, setUploads] = useState<UploadRecord[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    getRecentUploads()
      .then((result) => mounted && setUploads(result))
      .catch(() => mounted && setError("Recent uploads are unavailable right now."));
    return () => { mounted = false; };
  }, []);

  return (
    <section className="recent-uploads" aria-labelledby="recent-uploads-title">
      <div className="recent-uploads__heading">
        <div>
          <p className="eyebrow">Recent activity</p>
          <h2 id="recent-uploads-title">Continue an investigation.</h2>
        </div>
        <a className="text-link" href="/uploads">View Upload History <span aria-hidden="true">→</span></a>
      </div>

      {uploads === null && error === null && <div className="recent-uploads__loading" aria-label="Loading recent uploads"><span /><span /><span /></div>}
      {error && <p className="recent-uploads__message" role="status">{error}</p>}
      {uploads?.length === 0 && <p className="recent-uploads__message">No uploads have been returned by the service yet.</p>}
      {uploads && uploads.length > 0 && (
        <div className="recent-uploads__list">
          {uploads.map((upload) => (
            <a className="recent-upload" href={`/dashboard?uploadId=${upload.id}`} key={upload.id}>
              <span className="recent-upload__type">{upload.media_type}</span>
              <span className="recent-upload__name">{upload.original_filename}</span>
              <span className={`recent-upload__status recent-upload__status--${upload.status}`}>{upload.status}</span>
              <span className="recent-upload__date">{formatDate(upload.created_at)}</span>
            </a>
          ))}
        </div>
      )}
    </section>
  );
}
