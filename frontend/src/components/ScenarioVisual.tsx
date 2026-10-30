import type { Scenario } from '../app/demoTypes';

/** Lightweight, self-contained illustrated thumbnails. No external images or live feeds. */
export default function ScenarioVisual({ scenario }: { scenario: Scenario }) {
  const obstruction = scenario === 'CAR_BLOCKING' || scenario === 'MOTORCYCLE_BLOCKING' || scenario === 'BOARDING_FAILED';
  const motorbike = scenario === 'MOTORCYCLE_BLOCKING';
  const passenger = ['ASSISTANCE', 'ACKNOWLEDGED', 'BOARDING_COMPLETED', 'BOARDING_FAILED'].includes(scenario);
  const acknowledged = ['ACKNOWLEDGED', 'BOARDING_COMPLETED'].includes(scenario);
  const complete = scenario === 'BOARDING_COMPLETED';
  return (
    <div className={`scenario-visual visual-${scenario.toLowerCase()}`} aria-hidden="true">
      <svg viewBox="0 0 320 126" preserveAspectRatio="xMidYMid slice" focusable="false">
        <defs>
          <linearGradient id={`sky-${scenario}`} x1="0" x2="1" y1="0" y2="1"><stop stopColor="#e9f8ff"/><stop offset="1" stopColor="#d6f0ef"/></linearGradient>
          <linearGradient id={`road-${scenario}`} x1="0" y1="0" x2="1" y2="0"><stop stopColor="#334f70"/><stop offset="1" stopColor="#516a81"/></linearGradient>
        </defs>
        <rect width="320" height="126" fill={`url(#sky-${scenario})`}/>
        <circle cx="274" cy="21" r="36" fill="#fff" opacity=".35"/>
        <g fill="#b9d9e4" opacity=".85"><rect x="7" y="16" width="28" height="49" rx="2"/><rect x="38" y="6" width="36" height="59" rx="2"/><rect x="79" y="27" width="30" height="38" rx="2"/><rect x="236" y="15" width="35" height="50" rx="2"/><rect x="274" y="23" width="31" height="42" rx="2"/></g>
        <path d="M0 60H320V79H0Z" fill="#c2ddd4"/>
        <path d="M0 78H320V126H0Z" fill={`url(#road-${scenario})`}/>
        <path d="M0 80H320" stroke="#fff" strokeWidth="3"/>
        <path d="M12 112H79M99 112H166M186 112H253M273 112H313" stroke="#bdd4e0" strokeDasharray="30 9" strokeWidth="2"/>
        <path d="M169 63H307V80H169Z" fill={obstruction?'#ffe2db':'#a7eee0'} stroke={obstruction?'#e65855':'#23a894'} strokeWidth="1.5" strokeDasharray="5 4"/>
        <path d="M19 53H91V87H19Z" fill="#007d99" rx="4"/>
        <rect x="24" y="59" width="47" height="17" rx="3" fill="#b4e8f5"/>
        <rect x="74" y="59" width="12" height="23" rx="2" fill="#135b72"/>
        <path d="M38 59V76M53 59V76" stroke="#66b2c8" strokeWidth="2"/>
        <circle cx="34" cy="88" r="8" fill="#18354f" stroke="#fff" strokeWidth="2"/>
        <circle cx="78" cy="88" r="8" fill="#18354f" stroke="#fff" strokeWidth="2"/>
        <g transform="translate(117 42)"><rect x="0" y="3" width="3" height="28" fill="#497a87"/><rect x="-10" y="0" width="23" height="13" rx="3" fill="#246fe0"/><path d="M-5 6H9" stroke="#fff" strokeWidth="2"/></g>
        {passenger && <g transform="translate(145 63)"><circle cx="0" cy="-11" r="5" fill="#1c568a"/><path d="M0 -6L0 5L10 6" stroke="#1c568a" strokeWidth="3" fill="none" strokeLinecap="round"/><circle cx="-1" cy="11" r="7" stroke="#1c568a" fill="none" strokeWidth="2.5"/><path d="M9 6L15 15" stroke="#1c568a" strokeWidth="2.5"/></g>}
        {obstruction && !motorbike && <g transform="translate(231 67)"><path d="M-24 10L-16 -3H18L26 10Z" fill="#f16c5e"/><rect x="-30" y="8" width="60" height="18" rx="5" fill="#e35055"/><rect x="-15" y="0" width="29" height="9" rx="2" fill="#a7ddea"/><circle cx="-17" cy="26" r="6" fill="#263e52"/><circle cx="18" cy="26" r="6" fill="#263e52"/></g>}
        {motorbike && <g transform="translate(234 79)"><circle cx="-18" cy="12" r="9" stroke="#33475a" fill="none" strokeWidth="3"/><circle cx="19" cy="12" r="9" stroke="#33475a" fill="none" strokeWidth="3"/><path d="M-18 12L-2 -5L19 12L-1 12L-11 -1M-2 -5L5 -5" stroke="#ef8d35" strokeWidth="4" fill="none"/><circle cx="2" cy="-15" r="6" fill="#3a556e"/><path d="M3 -9L-2 0" stroke="#3a556e" strokeWidth="5"/></g>}
        {acknowledged && <g transform="translate(264 37)"><circle r="18" fill="#19a47f" stroke="white" strokeWidth="3"/><path d="M-8 0L-2 6L9 -7" stroke="white" strokeWidth="3.5" strokeLinecap="round" fill="none"/></g>}
        {scenario==='ASSISTANCE' && <g transform="translate(260 38)"><circle r="18" fill="#2373e9" stroke="white" strokeWidth="3"/><path d="M-4 -10V-3H4V2H-4L-8 8M3 2L8 9" stroke="white" strokeWidth="2.5" strokeLinecap="round" fill="none"/></g>}
        {complete && <path d="M169 63H307V80H169Z" fill="#82dfb2" opacity=".52"/>}
        {obstruction && <g><circle cx="291" cy="34" r="16" fill="#df4858" stroke="white" strokeWidth="3"/><path d="M291 26V35M291 41V42" stroke="white" strokeWidth="3" strokeLinecap="round"/></g>}
      </svg>
      <span className={`scenario-visual-status ${obstruction?'status-alert':complete?'status-success':'status-neutral'}`}>
        {obstruction?'Zone obstructed':complete?'Boarding complete':scenario==='ACKNOWLEDGED'?'Driver notified':scenario==='ASSISTANCE'?'Help requested':'Clear boarding zone'}
      </span>
    </div>
  );
}
