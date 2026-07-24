function normalizeServerTimestamp(value: string) {
  return /(?:Z|[+-]\d{2}:?\d{2})$/.test(value) ? value : `${value}Z`;
}

export function formatTimestamp(value: string) {
  const date = new Date(normalizeServerTimestamp(value));
  return Number.isNaN(date.getTime())
    ? "Timestamp unavailable"
    : date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

export function formatDate(value: string) {
  const date = new Date(normalizeServerTimestamp(value));
  return Number.isNaN(date.getTime())
    ? "Date unavailable"
    : date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export function formatTime(value: string) {
  const date = new Date(normalizeServerTimestamp(value));
  return Number.isNaN(date.getTime())
    ? "Time unavailable"
    : date.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}
