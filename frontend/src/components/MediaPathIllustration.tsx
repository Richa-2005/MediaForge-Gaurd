type MediaPath = "image" | "video" | "audio" | "text";

const shared = {
  viewBox: "0 0 160 112",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.2,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export function MediaPathIllustration({ type }: { type: MediaPath }) {
  if (type === "image") {
    return <svg className="media-path-illustration media-path-illustration--image" {...shared}>
      <text x="18" y="17">SOURCE</text><text x="87" y="17">FORENSIC OVERLAY</text>
      <rect x="18" y="24" width="55" height="60" rx="2" /><path d="m24 74 14-14 10 8 9-12 11 18M25 35h16M25 42h25" />
      <rect x="87" y="24" width="55" height="60" rx="2" /><path d="m93 74 14-14 10 8 9-12 11 18M94 35h16M94 42h25" />
      <rect className="media-path-illustration__heatmap" x="112" y="37" width="19" height="17" rx="1" /><circle className="media-path-illustration__scan" cx="121.5" cy="45.5" r="14" />
      <path className="media-path-illustration__annotation" d="M132 56l11 10M107 65h29" /><path className="media-path-illustration__trace" d="M18 96h124" />
    </svg>;
  }

  if (type === "video") {
    return <svg className="media-path-illustration media-path-illustration--video" {...shared}><rect x="26" y="25" width="92" height="58" rx="2" /><path d="m65 43 24 11-24 11z" /><path d="M35 17h70M35 91h70M35 13v8m17-8v8m17-8v8m17-8v8m17-8v8M35 87v8m17-8v8m17-8v8m17-8v8m17-8v8" /><path className="media-path-illustration__trace" d="M126 34v39M132 34v39" /><circle cx="129" cy="54" r="11" /></svg>;
  }

  if (type === "audio") {
    return <svg className="media-path-illustration media-path-illustration--audio" {...shared}><path d="M25 58h10l7-24 10 49 11-62 12 76 12-52 10 25h14l8-12 8 12h15" /><path d="M25 87h110" /><path d="M36 96v-7m10 7v-7m10 7v-7m10 7v-7m10 7v-7m10 7v-7m10 7v-7m10 7v-7m10 7v-7" /><circle className="media-path-illustration__pulse" cx="123" cy="58" r="16" /><path d="M118 58h10M123 53v10" /></svg>;
  }

  return <svg className="media-path-illustration media-path-illustration--text" {...shared}><path d="M34 22h66l18 18v50H34zM100 22v18h18M47 49h41M47 59h51M47 69h29" /><circle cx="121" cy="78" r="15" /><path d="m114 78 5 5 10-12" /><path className="media-path-illustration__trace" d="M27 94h76" /><circle cx="55" cy="94" r="2.5" /><circle cx="82" cy="94" r="2.5" /></svg>;
}
