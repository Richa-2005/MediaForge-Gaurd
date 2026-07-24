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
  { title: "Backend", items: ["FastAPI", "Uvicorn", "SQLAlchemy", "Pydantic", "Pydantic Settings", "HTTPX"] },
  { title: "AI / ML", items: ["OpenCV", "NumPy", "scikit-learn", "spaCy", "PyTorch", "TorchVision", "Transformers", "Sentence Transformers"] },
  { title: "Media forensics", items: ["Pillow", "python-magic", "Librosa", "MoviePy", "OpenAI Whisper"] },
  { title: "Text verification", items: ["LangDetect", "NLTK", "Wikipedia"] },
  { title: "Reporting", items: ["LangGraph", "LangChain Core", "Ollama", "Groq"] },
  { title: "Infrastructure", items: ["Celery", "Redis", "SQLite","PostgresSQL"] },
] as const;

export const teamMembers: TeamMember[] = [
  {
    name: "Richa Gupta",
    role: "Project contributor",
    bio: "",
    responsibilities: ["Backend & AI Systems"],
    initials: "RG",
    profiles: [{ label: "GitHub", href: "https://github.com/Richa-2005" }],
  },
  {
    name: "Rashmi Jha",
    role: "Project contributor",
    bio: "",
    responsibilities: ["AI & Machine Learning"],
    initials: "RJ",
    profiles: [{ label: "GitHub", href: "https://github.com/Rashmijha06" }],
  },
];

export const roadmapItems = [
  { title: "Adaptive evidence fusion", detail: "Strengthen cross-modal reasoning to produce more consistent verdicts across text, image, audio, and video analysis." },
  { title: "Trusted source expansion", detail: "Integrate additional verified news, fact-checking, and knowledge repositories for richer evidence retrieval." },
  { title: "Explainable AI insights", detail: "Provide transparent confidence breakdowns, forensic evidence attribution, and model decision explanations." },
  { title: "Real-time monitoring", detail: "Support continuous scanning of live media streams and URLs for emerging misinformation campaigns." },
  { title: "Model observability", detail: "Track per-agent runtime, detection confidence, evidence quality, and system performance through operational dashboards." },
  { title: "Scalable analysis pipeline", detail: "Expand specialized AI agents for advanced video forensics, audio tampering detection, metadata analysis, and multilingual verification." },
] as const;
