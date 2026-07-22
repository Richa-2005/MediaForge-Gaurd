type IconName = "image" | "video" | "audio" | "text" | "arrow" | "menu" | "close";

type IconProps = {
  name: IconName;
  size?: number;
  strokeWidth?: number;
};

export function Icon({ name, size = 20, strokeWidth = 1.6 }: IconProps) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  switch (name) {
    case "image":
      return <svg {...common}><rect x="3" y="4" width="18" height="16" rx="1.5" /><circle cx="8.5" cy="9" r="1.5" /><path d="m4.5 18 5.2-5 3.1 2.8 2.4-2.3 4.2 4.5" /></svg>;
    case "video":
      return <svg {...common}><rect x="3" y="5" width="13" height="14" rx="1.5" /><path d="m16 10 4-2v8l-4-2" /><path d="M7 9h4M7 15h4" /></svg>;
    case "audio":
      return <svg {...common}><path d="M4 12h2l2-5 3 10 2-7 2 3h5" /></svg>;
    case "text":
      return <svg {...common}><path d="M6 3.5h8l4 4V20.5H6z" /><path d="M14 3.5v4h4M9 12h6M9 16h6" /></svg>;
    case "arrow":
      return <svg {...common}><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
    case "menu":
      return <svg {...common}><path d="M4 7h16M4 12h16M4 17h16" /></svg>;
    case "close":
      return <svg {...common}><path d="m6 6 12 12M18 6 6 18" /></svg>;
  }
}
