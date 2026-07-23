type PassportMode = "idle" | "ready" | "processing";

export function MediaPassportIllustration({ mode }: { mode: PassportMode }) {
  const label = mode === "processing" ? "ANALYSIS RECORD" : mode === "ready" ? "MEDIA VERIFIED" : "MEDIA PASSPORT";

  return (
    <svg className={`media-passport-illustration media-passport-illustration--${mode}`} viewBox="0 0 520 340" fill="none" aria-hidden="true">
      <g className="media-passport-illustration__paper">
        <path d="M146 52h177l52 52v180H146z" />
        <path d="M323 52v52h52" />
        <rect x="174" y="93" width="84" height="70" rx="2" />
        <path d="m183 151 20-20 15 12 13-17 18 25M187 108h23M187 116h39" />
        <path d="M278 101h62M278 114h43M278 127h53M174 188h163M174 202h129M174 216h150" />
        <path d="M174 255h98M174 269h65" />
      </g>
      <g className="media-passport-illustration__metadata">
        <rect x="89" y="76" width="39" height="22" rx="1" /><rect x="89" y="109" width="39" height="22" rx="1" />
        <path d="M128 87h18M128 120h18" /><circle cx="99" cy="87" r="3" /><circle cx="99" cy="120" r="3" />
        <rect x="391" y="189" width="38" height="22" rx="1" /><path d="M375 200h16" /><circle cx="419" cy="200" r="3" />
      </g>
      <g className="media-passport-illustration__hash">
        <path d="M103 246h22m7 0h10m7 0h18m7 0h12m7 0h24" />
        <path d="M303 285h18m6 0h11m6 0h20m6 0h14" />
      </g>
      <g className="media-passport-illustration__signal">
        <circle cx="375" cy="104" r="22" /><path d="M364 104h22M375 93v22" />
        <path d="M375 126v32M375 158l28 25M375 158l-25 22" />
        <circle cx="403" cy="183" r="4" /><circle cx="350" cy="180" r="4" />
      </g>
      <text x="174" y="239">{label}</text>
    </svg>
  );
}
