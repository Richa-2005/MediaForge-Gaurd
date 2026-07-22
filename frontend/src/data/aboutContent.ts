export type ExternalProfile = {
  label: "LinkedIn" | "GitHub";
  href: string;
};

export type TeamMember = {
  name: string;
  role: string;
  bio: string;
  responsibilities: string[];
  initials: string;
  profiles: ExternalProfile[];
};

export const investigationStages = [
  { id: "01", name: "Media upload", note: "supported file or public URL" },
  { id: "02", name: "Media classification", note: "type and processing path" },
  { id: "03", name: "Media router", note: "preparation is selected" },
  { id: "04", name: "Specialized AI workers", note: "image / video / audio / text" },
  { id: "05", name: "Evidence collection", note: "outputs and artifacts are retained" },
  { id: "06", name: "LangGraph coordination", note: "context is assembled for reporting" },
  { id: "07", name: "Cross verification", note: "available signals are assessed" },
  { id: "08", name: "Summary generation", note: "structured explanation is formed" },
  { id: "09", name: "Investigation report", note: "Markdown report is persisted" },
] as const;

export const architectureLayers = [
  { label: "Frontend", detail: "React + Vite" },
  { label: "REST API", detail: "FastAPI" },
  { label: "Media router", detail: "submission services" },
  { label: "AI workers", detail: "media-specific paths" },
  { label: "Database", detail: "SQLAlchemy + SQLite" },
  { label: "LangGraph", detail: "report orchestration" },
  { label: "Summary engine", detail: "structured explanation" },
  { label: "Report generator", detail: "Markdown persistence" },
] as const;

export const technologyGroups = [
  { title: "Frontend", items: ["React", "TypeScript", "Vite"] },
  { title: "Backend", items: ["FastAPI", "SQLAlchemy", "Pydantic"] },
  { title: "AI / ML", items: ["OpenCV", "NumPy", "spaCy", "Transformers", "PyTorch", "LangGraph", "Ollama / Groq"] },
  { title: "Database", items: ["SQLite"] },
  { title: "Infrastructure", items: ["Celery", "Redis"] },
] as const;

export const teamMembers: TeamMember[] = [
  {
    name: "Richa Gupta",
    role: "Repository contributor",
    bio: "Identified as a contributor in the project commit history.",
    responsibilities: ["Project source contributions"],
    initials: "RG",
    profiles: [],
  },
  {
    name: "Rashmijha06",
    role: "Repository contributor",
    bio: "Identified as a contributor in the project commit history.",
    responsibilities: ["Project source contributions"],
    initials: "RJ",
    profiles: [{ label: "GitHub", href: "https://github.com/Rashmijha06" }],
  },
];

export const roadmapItems = [
  { title: "Improved multimodal reasoning", detail: "Broaden coordination between available media-specific findings." },
  { title: "Expanded verification sources", detail: "Extend the set of sources used by text verification paths." },
  { title: "Scalable deployment", detail: "Prepare the processing architecture for a larger operational footprint." },
  { title: "Additional media pipelines", detail: "Evaluate further specialist paths as they are implemented." },
  { title: "Enterprise integrations", detail: "Explore integrations only after the required backend interfaces exist." },
] as const;
