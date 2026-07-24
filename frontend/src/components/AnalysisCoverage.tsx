import type { CSSProperties } from "react";
import { Icon } from "./Icon";
import { MediaPathIllustration } from "./MediaPathIllustration";

const paths = [
  { title: "Image", copy: "Visual forensic analysis and processed-image metadata.", icon: "image" as const, visual: "image" as const },
  { title: "Video", copy: "Frame extraction and frame-based visual analysis.", icon: "video" as const, visual: "video" as const },
  { title: "Audio", copy: "Audio forensic analysis and available audio signals.", icon: "audio" as const, visual: "audio" as const },
  { title: "Text", copy: "Text analysis, claim verification, and supervisory fusion when available.", icon: "text" as const, visual: "text" as const },
];

export function AnalysisCoverage() {
  return (
    <section className="coverage section" aria-labelledby="coverage-title">
      <div className="container">
        <div className="coverage-surface scroll-reveal">
          <div className="section-intro">
            <p className="eyebrow type-on-scroll" style={{ "--type-chars": 24 } as CSSProperties}>Supported analysis paths</p>
            <h2 id="coverage-title" className="type-on-scroll type-on-scroll--heading" style={{ "--type-chars": 48 } as CSSProperties}>Built around the media you need to examine.</h2>
            <p className="section-intro__copy type-on-scroll type-on-scroll--copy" style={{ "--type-chars": 82 } as CSSProperties}>Each submission follows the available processing and analysis path for its media type.</p>
          </div>
          <div className="coverage-grid">
            {paths.map((path) => (
              <article className="coverage-item" key={path.title}>
                <MediaPathIllustration type={path.visual} />
                <span className="coverage-item__icon"><Icon name={path.icon} size={21} /></span>
                <h3>{path.title}</h3>
                <p>{path.copy}</p>
              </article>
            ))}
          </div>
          <a className="text-link text-link--section" href="/upload">Upload &amp; Analyze <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>
  );
}
