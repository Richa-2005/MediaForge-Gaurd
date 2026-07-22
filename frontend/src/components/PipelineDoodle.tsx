type PipelineDoodleProps = {
  stage: "upload" | "router" | "analysis" | "evidence" | "assessment" | "report";
};

const svgProps = {
  viewBox: "0 0 80 64",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.45,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export function PipelineDoodle({ stage }: PipelineDoodleProps) {
  switch (stage) {
    case "upload":
      return <svg {...svgProps}><rect x="10" y="20" width="60" height="34" rx="4" /><path d="M40 39V8m0 0-9 9m9-9 9 9M23 30h10M47 30h10" /><path d="M17 54v4m12-4v4m12-4v4m12-4v4" /></svg>;
    case "router":
      return <svg {...svgProps}><circle cx="40" cy="31" r="10" /><path d="M40 8v13M40 41v15M15 18l16 9M65 18 49 27M15 45l16-9M65 45l-16-9" /><circle cx="40" cy="7" r="2.5" /><circle cx="40" cy="57" r="2.5" /><circle cx="13" cy="17" r="2.5" /><circle cx="67" cy="17" r="2.5" /><circle cx="13" cy="46" r="2.5" /><circle cx="67" cy="46" r="2.5" /></svg>;
    case "analysis":
      return <svg {...svgProps}><rect x="7" y="10" width="26" height="19" rx="2" /><path d="m10 25 7-7 5 4 4-4 4 7M46 10h26v19H46zM51 19h16M12 44h17M12 50h17M48 50c3-11 7 11 10 0s7 11 10 0" /><path d="M43 38v19" /></svg>;
    case "evidence":
      return <svg {...svgProps}><path d="M8 21h25l5 6h34v27H8z" /><path d="M8 21v-6h23l7 6" /><path d="M23 37h34M23 44h24" /><circle cx="17" cy="37" r="2" /><circle cx="17" cy="44" r="2" /></svg>;
    case "assessment":
      return <svg {...svgProps}><path d="M14 48V25m13 23V14m13 34V31m13 17V9m13 39V22" /><path d="M9 53h62" /><circle cx="53" cy="9" r="4" /><path d="m51 9 1.5 1.5L56 7" /></svg>;
    case "report":
      return <svg {...svgProps}><path d="M21 7h29l12 12v38H21z" /><path d="M50 7v12h12M30 30h23M30 38h23M30 46h15" /><path d="m15 47 4 4 8-9" /></svg>;
  }
}
