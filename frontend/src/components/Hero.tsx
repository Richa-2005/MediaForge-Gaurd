import { Icon } from "./Icon";
import { MediaIntakePanel } from "./MediaIntakePanel";

export function Hero() {
  return (
    <section className="hero section" aria-labelledby="hero-title">
      <div className="container hero__grid">
        <div className="hero__content">
          <p className="eyebrow reveal">Media authenticity analysis</p>
          <h1 id="hero-title" className="hero__title reveal reveal--delay-1">Examine media before you trust it.</h1>
          <p className="hero__copy reveal reveal--delay-2">
            MediaForge Guard helps you submit supported media, follow its analysis, and review the available evidence in one clear workflow.
          </p>
          <div className="hero__actions reveal reveal--delay-3">
            <a className="button button--primary" href="/upload">
              <span>Upload &amp; Analyze</span>
              <Icon name="arrow" size={17} />
            </a>
            <a className="text-link" href="/dashboard">Open Dashboard <Icon name="arrow" size={16} /></a>
          </div>
          <p className="hero__scope reveal reveal--delay-4">Image <span>·</span> Video <span>·</span> Audio <span>·</span> Text</p>
        </div>
        <MediaIntakePanel />
      </div>
    </section>
  );
}
