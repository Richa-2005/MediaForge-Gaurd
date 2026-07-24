import { useState } from "react";
import type { UploadRecord } from "../types/upload";
import { formatTimestamp } from "../utils/dateTime";
import { StatusBadge } from "./StatusBadge";
import { InvestigationBoardBackdrop } from "./InvestigationBoardBackdrop";

type InvestigationSelectorProps = {
  uploads: UploadRecord[] | null;
  selectedId: number | null;
  onSelect: (uploadId: number) => void;
  loading: boolean;
  error: string | null;
};

export function InvestigationSelector({ uploads, selectedId, onSelect, loading, error }: InvestigationSelectorProps) {
  const [showAll, setShowAll] = useState(false);
  const visibleUploads = showAll ? uploads : uploads?.slice(0, 5);
  const hiddenCount = uploads ? Math.max(uploads.length - 5, 0) : 0;

  return (
    <section className="investigation-selector" aria-labelledby="investigation-selector-title">
      <InvestigationBoardBackdrop />
      <div className="investigation-selector__heading">
        <div>
          <p className="eyebrow">Investigation dashboard</p>
          <h1 id="investigation-selector-title">Review an active investigation.</h1>
        </div>
        <a className="button button--primary" href="/upload">New investigation</a>
      </div>
      <p className="investigation-selector__copy">Select a recent submission to inspect the processing record, available evidence, specialist findings, and report status.</p>
      <h2 className="investigation-selector__section-title">Your Previous Investigations</h2>

      {loading && <div className="selector-loading" aria-label="Loading recent investigations"><span /><span /><span /></div>}
      {error && <p className="selector-message" role="alert">{error}</p>}
      {uploads?.length === 0 && <p className="selector-message">No submitted media is available to investigate yet.</p>}
      {uploads && uploads.length > 0 && (
        <>
          <div className="investigation-selector__list" aria-label="Recent investigations">
          {visibleUploads?.map((upload) => (
            <article
              key={upload.id}
              className={`investigation-choice ${selectedId === upload.id ? "investigation-choice--selected" : ""}`}
            >
              <button type="button" onClick={() => onSelect(upload.id)} aria-pressed={selectedId === upload.id}>
                <span className="investigation-choice__media">{upload.media_type}</span>
                <span className="investigation-choice__name">{upload.original_filename}</span>
                <span className="investigation-choice__time">{formatTimestamp(upload.created_at)}</span>
                <StatusBadge status={upload.status} />
              </button>
              <a className="investigation-choice__results" href={`/results?uploadId=${upload.id}`}>Review results <span aria-hidden="true">→</span></a>
            </article>
          ))}
          </div>
          {hiddenCount > 0 && <button className="quiet-button investigation-selector__more" type="button" onClick={() => setShowAll((current) => !current)}>{showAll ? "Show fewer" : `See more (${hiddenCount})`}</button>}
        </>
      )}
    </section>
  );
}
