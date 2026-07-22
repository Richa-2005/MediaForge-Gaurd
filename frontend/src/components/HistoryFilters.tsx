import type { UploadStatus } from "../types/upload";

type HistoryFiltersProps = {
  query: string;
  mediaType: string;
  status: string;
  mediaTypes: string[];
  statuses: UploadStatus[];
  onQueryChange: (value: string) => void;
  onMediaTypeChange: (value: string) => void;
  onStatusChange: (value: string) => void;
};

export function HistoryFilters({ query, mediaType, status, mediaTypes, statuses, onQueryChange, onMediaTypeChange, onStatusChange }: HistoryFiltersProps) {
  return (
    <section className="history-filters" aria-label="Filter recent investigations">
      <label className="history-search"><span>Search recent investigations</span><input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Search by file name" /></label>
      <label><span>Media type</span><select value={mediaType} onChange={(event) => onMediaTypeChange(event.target.value)}><option value="">All media</option>{mediaTypes.map((type) => <option value={type} key={type}>{type}</option>)}</select></label>
      <label><span>Status</span><select value={status} onChange={(event) => onStatusChange(event.target.value)}><option value="">All statuses</option>{statuses.map((item) => <option value={item} key={item}>{item}</option>)}</select></label>
    </section>
  );
}
