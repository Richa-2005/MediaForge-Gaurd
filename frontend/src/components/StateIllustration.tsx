type StateIllustrationKind = "results" | "evidence" | "archive";

export function StateIllustration({ kind }: { kind: StateIllustrationKind }) {
  if (kind === "archive") {
    return <svg className="state-illustration state-illustration--archive" viewBox="0 0 180 112" fill="none" aria-hidden="true"><path d="M35 38h40l8 9h62v38H35zM35 38v-10h36l12 10" /><path d="M57 64h59M57 73h42" /><circle cx="50" cy="64" r="3" /><circle cx="50" cy="73" r="3" /><path className="state-illustration__trace" d="M27 95h115" /><circle cx="127" cy="29" r="15" /><path d="m120 29 5 5 10-12" /></svg>;
  }
  if (kind === "evidence") {
    return <svg className="state-illustration state-illustration--evidence" viewBox="0 0 180 112" fill="none" aria-hidden="true"><rect x="38" y="23" width="70" height="54" rx="2" /><path d="m47 67 16-16 12 10 11-13 13 19" /><circle cx="119" cy="60" r="18" /><path d="M132 73l14 14M110 60h18M119 51v18" /><path className="state-illustration__trace" d="M29 91h94" /><circle cx="47" cy="91" r="3" /><circle cx="84" cy="91" r="3" /></svg>;
  }
  return <svg className="state-illustration state-illustration--results" viewBox="0 0 180 112" fill="none" aria-hidden="true"><path d="M47 18h60l22 22v53H47zM107 18v22h22M61 54h53M61 64h42M61 74h31" /><circle cx="132" cy="80" r="17" /><path d="m124 80 6 6 11-14" /><path className="state-illustration__trace" d="M36 95h82" /></svg>;
}
