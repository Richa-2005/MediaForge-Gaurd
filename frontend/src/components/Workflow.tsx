import { useEffect, useRef, useState } from "react";
import type { CSSProperties } from "react";
import { WorkflowProductShowcase } from "./WorkflowProductShowcase";

const stages = [
  { number: "01", title: "Upload media", summary: "Supported file or public URL", detailTitle: "A single intake, routed by media type.", detail: "The submitted file is MIME-checked, hashed, stored, and queued for processing before analysis begins.", technologies: ["MIME validation", "SHA-256 deduplication", "Queued processing"], doodle: "upload" as const },
  { number: "02", title: "Media classification", summary: "The appropriate path is selected", detailTitle: "Each medium receives the right investigation path.", detail: "The incoming submission is classified before images, video, audio, or text are prepared for their available analysis path.", technologies: ["Image routing", "Frame extraction", "Audio preparation", "UTF-8 text validation"], doodle: "router" as const },
  { number: "03", title: "AI investigation", summary: "Purpose-built forensic pipelines", detailTitle: "Relevant signals are examined for the submitted media.", detail: "Available specialist analysis examines media-specific signals and returns observations with the context needed for review.", technologies: ["Image forensics", "Frame analysis", "Audio signals", "Text and claim analysis"], doodle: "analysis" as const },
  { number: "04", title: "Evidence collection", summary: "Agent output becomes reviewable evidence", detailTitle: "Outputs are retained with their context.", detail: "Analysis results, evidence items, per-frame details, and processing artifacts are persisted for the submission’s review record.", technologies: ["Agent evidence", "Artifact metadata", "Per-frame results", "Analysis persistence"], doodle: "evidence" as const },
  { number: "05", title: "LangGraph reasoning", summary: "Context is assembled for reporting", detailTitle: "The report is grounded in the available record.", detail: "LangGraph collects persisted investigation context, forms a structured explanation, and keeps the reported reasoning separate from the underlying assessment.", technologies: ["Context collection", "Structured explanation", "Report formatting", "Persisted reasoning"], doodle: "assessment" as const },
  { number: "06", title: "Investigation report", summary: "A structured review record", detailTitle: "The final report remains inspectable.", detail: "The completed report presents the available verdict, confidence, findings, limitations, and recommended next action for careful review.", technologies: ["Verdict", "Confidence", "Key findings", "Limitations"], doodle: "report" as const },
];

export function Workflow() {
  const [activeStage, setActiveStage] = useState(0);
  const sectionRef = useRef<HTMLElement | null>(null);
  const active = stages[activeStage];

  useEffect(() => {
    const updateStageFromScroll = () => {
      const section = sectionRef.current;
      if (!section) return;

      const bounds = section.getBoundingClientRect();
      if (bounds.bottom < 0 || bounds.top > window.innerHeight) return;

      const distance = Math.max(section.offsetHeight - window.innerHeight * 0.25, 1);
      const progress = Math.min(1, Math.max(0, (window.innerHeight * 0.55 - bounds.top) / distance));
      setActiveStage(Math.min(stages.length - 1, Math.floor(progress * stages.length)));
    };

    updateStageFromScroll();
    window.addEventListener("scroll", updateStageFromScroll, { passive: true });
    window.addEventListener("resize", updateStageFromScroll);
    return () => {
      window.removeEventListener("scroll", updateStageFromScroll);
      window.removeEventListener("resize", updateStageFromScroll);
    };
  }, []);

  return (
    <section className="workflow section section--wide" aria-labelledby="workflow-title" ref={sectionRef}>
      <div className="container">
        <div className="section-intro section-intro--workflow">
          <p className="eyebrow scroll-reveal">Verification pipeline</p>
          <h2 id="workflow-title" className="scroll-reveal">A complete investigation system, not a single model.</h2>
          <p className="section-intro__copy scroll-reveal">Follow the path from secure media intake through specialized analysis, evidence, assessment, and structured reporting.</p>
        </div>

        <div className="workflow-showcase-layout">
          <div className="pipeline" style={{ "--pipeline-progress": `${(activeStage / (stages.length - 1)) * 100}%` } as CSSProperties}>
            <div className="pipeline__track" aria-hidden="true"><span /></div>
            <div className="pipeline__sequence" aria-label="Verification pipeline stages">
              {stages.map((stage, index) => (
                <button
                  className={`pipeline-stage ${index === activeStage ? "pipeline-stage--active" : ""} ${index < activeStage ? "pipeline-stage--complete" : ""}`}
                  key={stage.number}
                  type="button"
                  aria-pressed={index === activeStage}
                  aria-controls="pipeline-detail"
                  onClick={() => setActiveStage(index)}
                >
                  <span className="pipeline-stage__node"><span>{stage.number}</span></span>
                  <span className="pipeline-stage__copy"><strong>{stage.title}</strong><small>{stage.summary}</small></span>
                </button>
              ))}
            </div>
          </div>

          <article className="pipeline-detail" id="pipeline-detail" aria-live="polite">
            <div className="pipeline-detail__illustration"><WorkflowProductShowcase key={active.number} stage={active.doodle} /></div>
            <div className="pipeline-detail__content">
              <p className="pipeline-detail__index">{active.number} / {String(stages.length).padStart(2, "0")}</p>
              <h3>{active.detailTitle}</h3>
              <p>{active.detail}</p>
              <ul aria-label={`${active.title} technologies`}>
                {active.technologies.map((technology) => <li key={technology}>{technology}</li>)}
              </ul>
            </div>
          </article>
        </div>

        <a className="text-link text-link--section scroll-reveal" href="/upload">Begin an analysis <span aria-hidden="true">→</span></a>
      </div>
    </section>
  );
}
