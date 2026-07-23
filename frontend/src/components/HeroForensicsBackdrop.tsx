export function HeroForensicsBackdrop() {
  return (
    <div className="hero-forensics-backdrop" aria-hidden="true">
      <svg viewBox="0 0 960 620" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g className="hero-forensics-backdrop__frame">
          <path d="M91 151V96h55M814 96h55v55M869 469v55h-55M146 524H91v-55" />
          <rect x="146.5" y="96.5" width="668" height="428" rx="2" />
          <path d="M146 410h668M279 96v428M682 96v428" />
        </g>
        <rect className="hero-forensics-backdrop__scan" x="154" y="106" width="1.5" height="408" rx=".75" />

        <g className="hero-forensics-backdrop__signal">
          <path d="M112 312h58l23-43 35 93 39-142 34 178 37-86 30 44h48l33-63 29 105 35-186 40 149 28-49h74" />
          <circle cx="193" cy="269" r="5" />
          <circle cx="377" cy="356" r="5" />
          <circle cx="568" cy="212" r="5" />
          <circle cx="786" cy="312" r="5" />
        </g>

        <g className="hero-forensics-backdrop__evidence">
          <path d="M191 183h54M191 197h87M191 211h39" />
          <path d="M716 406h48M716 420h65M716 434h31" />
          <rect x="213.5" y="369.5" width="86" height="72" rx="1" />
          <circle cx="256" cy="397" r="11.5" />
          <path d="m221 432 21-19 15 12 14-15 20 22" />
          <path d="M606 174h83v83h-83zM626 216h43M647.5 194v44" />
        </g>

        <g className="hero-forensics-backdrop__video">
          <rect x="321.5" y="129.5" width="167" height="106" rx="2" />
          <path d="m391 168 36 14-36 14z" />
          <path d="M337 145h31M337 219h54M457 145h15M458 219h14" />
          <path d="M321 260h167M321 274h113M321 288h141" />
        </g>

        <g className="hero-forensics-backdrop__face-scan">
          <circle cx="547" cy="385" r="58.5" />
          <path d="M506 357v-14h14M574 343h14v14M588 413v14h-14M520 427h-14v-14" />
          <path d="M526 382h9M559 382h9M539 406h19" />
          <circle cx="530.5" cy="382" r="2" /><circle cx="563.5" cy="382" r="2" />
        </g>

        <g className="hero-forensics-backdrop__spectrum">
          <path d="M166 466h93" />
          <rect x="174" y="446" width="5" height="12" /><rect x="185" y="431" width="5" height="27" />
          <rect x="196" y="415" width="5" height="43" /><rect x="207" y="438" width="5" height="20" />
          <rect x="218" y="423" width="5" height="35" /><rect x="229" y="443" width="5" height="15" />
          <rect x="240" y="433" width="5" height="25" />
        </g>

        <g className="hero-forensics-backdrop__text-analysis">
          <path d="M694 296h95M694 310h62M694 324h84M694 338h45M694 352h72" />
          <circle cx="775" cy="370" r="14.5" />
          <path d="m768 370 5 5 10-12" />
        </g>

        <g className="hero-forensics-backdrop__nodes">
          <circle cx="279" cy="410" r="4.5" />
          <circle cx="468" cy="398" r="4.5" />
          <circle cx="647" cy="216" r="4.5" />
          <path d="M284 410h179M472 395l170-175" />
        </g>

        <g className="hero-forensics-backdrop__noise">
          <path d="M120 246h11M129 254h7M747 142h14M761 151h9M731 472h12M741 480h8M350 476h10M357 484h7" />
          <circle cx="298" cy="327" r="2" /><circle cx="304" cy="334" r="1.5" /><circle cx="294" cy="338" r="1.5" />
          <circle cx="705" cy="244" r="2" /><circle cx="713" cy="250" r="1.5" /><circle cx="700" cy="255" r="1.5" />
        </g>
      </svg>
    </div>
  );
}
