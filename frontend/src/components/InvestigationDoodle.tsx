import type { CSSProperties } from "react";
import { investigationStages } from "../data/aboutContent";

export function InvestigationDoodle() {
  return (
    <section className="case-flow section" aria-labelledby="case-flow-title">
      <div className="container">
        <div className="case-flow__heading">
          <p className="eyebrow">Investigation workflow</p>
          <h2 id="case-flow-title">How MediaForge Guard works.</h2>
          <p>An investigation moves through implemented intake, analysis, persistence, and report-generation paths. Each step is retained against the submission record.</p>
        </div>

        <figure className="investigation-doodle" aria-labelledby="case-flow-title">
          <figcaption className="sr-only">MediaForge Guard investigation flow, from upload through specialist workers, evidence collection, LangGraph coordination, and final report.</figcaption>
          <span className="investigation-doodle__margin-note investigation-doodle__margin-note--top">field notes / a traceable record</span>
          <span className="investigation-doodle__shape investigation-doodle__shape--one" aria-hidden="true">*</span>
          <span className="investigation-doodle__shape investigation-doodle__shape--two" aria-hidden="true">~</span>
          <ol className="investigation-doodle__stages">
            {investigationStages.map((stage, index) => (
              <li className={`investigation-doodle__stage investigation-doodle__stage--${index + 1} scroll-reveal`} key={stage.id} style={{ "--item-index": index } as CSSProperties}>
                <span className="investigation-doodle__marker">{stage.id}</span>
                <span className="investigation-doodle__copy"><strong>{stage.name}</strong><small>{stage.note}</small></span>
              </li>
            ))}
          </ol>
          <div className="investigation-doodle__workers scroll-reveal" style={{ "--item-index": 3 } as CSSProperties} aria-label="Specialized analysis workers">
            <span>Image analysis</span><span>Video analysis</span><span>Audio analysis</span><span>Text analysis</span>
          </div>
          <span className="investigation-doodle__annotation investigation-doodle__annotation--workers">only the relevant worker path is used</span>
          <span className="investigation-doodle__annotation investigation-doodle__annotation--report">report explains available results; it does not replace review</span>
        </figure>
      </div>
    </section>
  );
}
