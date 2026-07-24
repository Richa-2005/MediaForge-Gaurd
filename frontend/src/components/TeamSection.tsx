import { teamMembers, type ExternalProfile } from "../data/aboutContent";

function ProfileGlyph({ label }: { label: ExternalProfile["label"] }) {
  if (label === "LinkedIn") {
    return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.2 7.5A2.3 2.3 0 1 0 5.2 3a2.3 2.3 0 0 0 0 4.5ZM3.2 20.8h4V9.2h-4v11.6ZM9.6 9.2v11.6h4v-5.7c0-1.5.3-2.9 2.2-2.9 1.8 0 1.8 1.7 1.8 3v5.6h4v-6.4c0-3.1-.7-5.5-4.3-5.5-1.7 0-2.9.9-3.4 1.8h-.1V9.2h-3.8Z" fill="currentColor" /></svg>;
  }
  return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.7a9.3 9.3 0 0 0-2.9 18.1c.5.1.6-.2.6-.5v-1.8c-2.5.5-3-1.1-3-1.1-.4-1-1-1.3-1-1.3-.8-.5.1-.5.1-.5.9.1 1.4.9 1.4.9.8 1.4 2.1 1 2.6.8.1-.6.3-1 .6-1.2-2-.2-4.1-1-4.1-4.5 0-1 .4-1.8.9-2.4-.1-.2-.4-1.1.1-2.4 0 0 .8-.2 2.5.9a8.5 8.5 0 0 1 4.6 0c1.7-1.1 2.5-.9 2.5-.9.5 1.3.2 2.2.1 2.4.6.6.9 1.4.9 2.4 0 3.5-2.1 4.3-4.1 4.5.3.3.6.9.6 1.8v2.7c0 .3.2.6.6.5A9.3 9.3 0 0 0 12 2.7Z" fill="currentColor" /></svg>;
}

export function TeamSection() {
  return (
    <section className="case-team section" aria-labelledby="case-team-title">
      <div className="container">
        <div className="case-team__heading"><p className="eyebrow">Meet the engineers</p><h2 id="case-team-title">The people recorded in the project history.</h2></div>
        <div className="team-grid">
          {teamMembers.map((member) => <article className="team-card scroll-reveal" key={member.name}>
            <div className="team-card__identity"><p>{member.role}</p><h3>{member.name}</h3></div>
            <div className="team-card__responsibilities"><span>Primary responsibility</span><ul>{member.responsibilities.map((item) => <li key={item}>{item}</li>)}</ul></div>
            {member.profiles.length > 0 && <div className="team-card__profiles" aria-label={`${member.name} profiles`}>{member.profiles.map((profile) => <a href={profile.href} target="_blank" rel="noreferrer" key={profile.label}><ProfileGlyph label={profile.label} /><span>{profile.label}</span><span className="sr-only"> (opens in a new tab)</span></a>)}</div>}
          </article>)}
        </div>
      </div>
    </section>
  );
}
