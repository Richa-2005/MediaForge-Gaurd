import { technologyGroups } from "../data/aboutContent";

export function TechnologyStack() {
  return <section className="case-stack section" aria-labelledby="case-stack-title"><div className="container"><div className="case-stack__heading"><p className="eyebrow">Technology stack</p><h2 id="case-stack-title">Tools already present in the implementation.</h2></div><div className="technology-groups">{technologyGroups.map((group) => <article className="technology-group scroll-reveal" key={group.title}><h3>{group.title}</h3><ul>{group.items.map((item) => <li key={item}>{item}</li>)}</ul></article>)}</div></div></section>;
}
