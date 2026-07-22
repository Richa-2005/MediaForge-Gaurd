import { roadmapItems } from "../data/aboutContent";

export function RoadmapTimeline() {
  return <section className="case-roadmap section" aria-labelledby="case-roadmap-title"><div className="container case-roadmap__layout"><div className="case-roadmap__intro"><p className="eyebrow">Future work</p><h2 id="case-roadmap-title">Where the investigation system can go next.</h2><p>These are proposed directions, not capabilities currently available in MediaForge Guard.</p></div><ol className="roadmap-timeline">{roadmapItems.map((item, index) => <li className="scroll-reveal" key={item.title}><span>{String(index + 1).padStart(2, "0")}</span><div><h3>{item.title}</h3><p>{item.detail}</p></div></li>)}</ol></div></section>;
}
