type MediaType = "image" | "video" | "audio" | "text" | string;

export function ProcessingSketch({ mediaType }: { mediaType: MediaType }) {
  if (mediaType === "video") return <svg className="processing-sketch" viewBox="0 0 90 72" fill="none" aria-hidden="true"><rect x="18" y="14" width="46" height="34" rx="2" /><path d="m37 25 13 6-13 6zM24 8v6m10-6v6m10-6v6m10-6v6M24 48v6m10-6v6m10-6v6m10-6v6" /><path className="processing-sketch__trace" d="M18 60h52" /><circle cx="67" cy="31" r="8" /></svg>;
  if (mediaType === "audio") return <svg className="processing-sketch" viewBox="0 0 90 72" fill="none" aria-hidden="true"><path d="M12 38h8l5-14 7 30 7-42 7 48 7-32 6 16h9l5-9 5 9h8" /><path d="M13 59h64" /><path className="processing-sketch__trace" d="M20 65v-5m9 5v-8m9 8v-13m9 13v-9m9 9v-15m9 15v-7" /><circle cx="70" cy="38" r="9" /></svg>;
  if (mediaType === "text") return <svg className="processing-sketch" viewBox="0 0 90 72" fill="none" aria-hidden="true"><path d="M23 10h37l13 13v38H23zM60 10v13h13M32 32h26M32 39h31M32 46h18" /><circle cx="68" cy="52" r="10" /><path d="m63 52 4 4 7-9" /><path className="processing-sketch__trace" d="M14 62h47" /></svg>;
  return <svg className="processing-sketch" viewBox="0 0 90 72" fill="none" aria-hidden="true"><rect x="16" y="13" width="49" height="38" rx="2" /><path d="m22 44 12-12 9 7 8-10 9 15M23 22h15" /><circle cx="58" cy="25" r="8" /><path d="m64 31 9 9M54 25h8M58 21v8" /><path className="processing-sketch__trace" d="M12 60h54" /></svg>;
}

export function ReportAssemblyIllustration() {
  return <svg className="report-assembly-illustration" viewBox="0 0 310 170" fill="none" aria-hidden="true"><g className="report-assembly-illustration__pages"><path d="M88 22h111l34 34v91H88zM199 22v34h34M108 77h91M108 92h75M108 107h83M108 122h51" /><path d="M73 38h111M73 38v91M73 129h111" /></g><g className="report-assembly-illustration__signals"><circle cx="48" cy="62" r="8" /><circle cx="48" cy="100" r="8" /><path d="M56 62h31M56 100h31M41 62h14M48 55v14M43 100l4 4 7-9" /></g><g className="report-assembly-illustration__check"><circle cx="255" cy="124" r="18" /><path d="m246 124 7 7 12-15" /></g></svg>;
}
