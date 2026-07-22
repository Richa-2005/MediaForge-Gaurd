import { architectureLayers } from "../data/aboutContent";

export function ArchitectureDiagram() {
  return (
    <section className="case-architecture section" aria-labelledby="case-architecture-title">
      <div className="container">
        <div className="case-architecture__heading">
          <p className="eyebrow">Engineering architecture</p>
          <h2 id="case-architecture-title">A system of focused layers, not a black box.</h2>
          <p>The browser application reads and writes through the API. Background workers create analysis records; the report workflow builds on the persisted primary result.</p>
        </div>
        <ol className="architecture-diagram" aria-label="Implemented MediaForge Guard architecture">
          {architectureLayers.map((layer, index) => (
            <li className="architecture-diagram__node scroll-reveal" key={layer.label}>
              <span className="architecture-diagram__index">{String(index + 1).padStart(2, "0")}</span>
              <strong>{layer.label}</strong>
              <small>{layer.detail}</small>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
