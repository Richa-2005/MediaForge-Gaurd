type WorkflowProductShowcaseProps = {
  stage: "upload" | "router" | "analysis" | "evidence" | "assessment" | "report";
};

const labels = {
  upload: "Media intake",
  router: "Media routing",
  analysis: "Specialist analysis",
  evidence: "Evidence record",
  assessment: "LangGraph reasoning",
  report: "Investigation report",
} as const;

export function WorkflowProductShowcase({ stage }: WorkflowProductShowcaseProps) {
  return (
    <div className={`workflow-showcase workflow-showcase--${stage}`} aria-hidden="true">
      <div className="workflow-showcase__screen">
        <div className="workflow-showcase__topbar">
          <span className="workflow-showcase__signal" />
          <span>{labels[stage]}</span>
          <i /><i />
        </div>

        {stage === "upload" && <div className="workflow-showcase__intake"><span>+</span><strong>media.jpg</strong><small>Ready to analyze</small></div>}

        {stage === "router" && <div className="workflow-showcase__router"><span className="workflow-showcase__source">MEDIA</span><i /><b>AI</b><i /><span className="workflow-showcase__route">VISION</span><span className="workflow-showcase__route">AUDIO</span><span className="workflow-showcase__route">TEXT</span></div>}

        {stage === "analysis" && <div className="workflow-showcase__analysis"><article><span>VISION</span><i /><i /><b /></article><article><span>FORENSICS</span><i /><i /><b /></article><article><span>CONTEXT</span><i /><i /><b /></article></div>}

        {stage === "evidence" && <div className="workflow-showcase__evidence"><div><i /><i /><i /></div><article><span>Artifact record</span><b /><b /><b /></article><small>3 evidence items retained</small></div>}

        {stage === "assessment" && <div className="workflow-showcase__reasoning"><span>CONTEXT</span><i /><b>EXPLAIN</b><i /><span>FORMAT</span><i /><strong>REPORT</strong></div>}

        {stage === "report" && <div className="workflow-showcase__report"><span>INVESTIGATION REPORT</span><i /><i /><i /><div><b>✓</b><small>Evidence reviewed</small></div></div>}
      </div>
      <span className="workflow-showcase__caption">Product view</span>
    </div>
  );
}
