export const photos={
  "city": {
    "src": "/photos/city-streets.jpg",
    "alt": "A red city bus passing a busy Kuala Lumpur terminal and shophouses",
    "credit": "Haiqal Hadi",
    "url": "https://www.pexels.com/photo/busy-street-scene-in-kuala-lumpur-with-buses-33449462/",
    "width": 1600,
    "height": 906,
    "small": "/photos/responsive/city-streets-640.webp",
    "position": "50% 50%"
  },
  "driver": {
    "src": "/photos/driver-view.jpg",
    "alt": "A driver’s hand at the wheel of a bus in warm daylight",
    "credit": "Lê Minh",
    "url": "https://www.pexels.com/photo/person-hand-on-steering-wheel-977213/",
    "width": 1600,
    "height": 1067,
    "small": "/photos/responsive/driver-view-640.webp",
    "position": "50% 50%"
  },
  "skyline": {
    "src": "/photos/kl-skyline.jpg",
    "alt": "Rail tracks leading towards the Kuala Lumpur skyline",
    "credit": "Alfisyah Molis",
    "url": "https://www.pexels.com/photo/kuala-lumpur-skyline-with-metro-rail-track-37014908/",
    "width": 1600,
    "height": 2133,
    "small": "/photos/responsive/kl-skyline-640.webp",
    "position": "50% 50%"
  },
  "bus": {
    "src": "/photos/kuala-lumpur-bus.jpg",
    "alt": "A public bus on a Kuala Lumpur street",
    "credit": "Theodore Nguyen",
    "url": "https://www.pexels.com/photo/bus-in-kuala-lumpur-27023374/",
    "width": 1400,
    "height": 2100,
    "small": "/photos/responsive/kuala-lumpur-bus-640.webp",
    "position": "50% 50%"
  },
  "access": {
    "src": "/photos/accessible-bus-stop.jpg",
    "alt": "Passengers waiting at a bus stop, including a person using a rollator walker",
    "credit": "Wheeleo Walker",
    "url": "https://www.pexels.com/photo/urban-bus-stop-with-people-and-rollator-walker-33120790/",
    "width": 1400,
    "height": 933,
    "small": "/photos/responsive/accessible-bus-stop-640.webp",
    "position": "50% 50%"
  },
  "people": {
    "src": "/photos/commuter-journeys.jpg",
    "alt": "Passengers sharing an everyday bus journey",
    "credit": "Jenkin Shen",
    "url": "https://www.pexels.com/photo/commuters-traveling-on-a-city-bus-30094326/",
    "width": 1400,
    "height": 933,
    "small": "/photos/responsive/commuter-journeys-640.webp",
    "position": "50% 50%"
  },
  "evening": {
    "src": "/photos/kl-evening-stop.jpg",
    "alt": "Passengers waiting beside a bus at a Kuala Lumpur stop at night",
    "credit": "Theodore Nguyen",
    "url": "https://www.pexels.com/photo/people-on-bus-stop-at-night-26725631/",
    "position": "50% 48%",
    "width": 1400,
    "height": 2100,
    "small": "/photos/responsive/kl-evening-stop-640.webp"
  },
  "wheelchair": {
    "src": "/photos/wheelchair-journey.jpg",
    "alt": "A wheelchair user waiting beside a bus shelter in Delft, Netherlands",
    "credit": "Rollz International",
    "url": "https://www.pexels.com/photo/woman-on-wheelchair-sitting-at-bus-stop-19903109/",
    "position": "48% 53%",
    "width": 1400,
    "height": 781,
    "small": "/photos/responsive/wheelchair-journey-640.webp"
  },
  "door": {
    "src": "/photos/accessible-bus-door.jpg",
    "alt": "Wheelchair accessibility and elderly passenger symbols beside a red bus door",
    "credit": "Craig Adderley",
    "url": "https://www.pexels.com/photo/red-bus-with-accessibility-and-elderly-symbols-29163033/",
    "position": "50% 52%",
    "width": 1400,
    "height": 933,
    "small": "/photos/responsive/accessible-bus-door-640.webp"
  },
  "commuters": {
    "src": "/photos/kl-commuters.jpg",
    "alt": "A black-and-white photograph of passengers beside a Rapid KL bus at a terminal",
    "credit": "Vince Cruz",
    "url": "https://www.pexels.com/photo/people-standing-by-coach-bus-19148497/",
    "position": "50% 50%",
    "width": 1400,
    "height": 1867,
    "small": "/photos/responsive/kl-commuters-640.webp"
  }
} as const;
export type PhotoName=keyof typeof photos;
export function photoSources(photo:PhotoName){const p=photos[photo];return `${p.small} 640w, ${p.src} ${p.width}w`}
export default function TransitPhoto({photo='bus',title='Everyday journeys. Better connected.',subtitle='Designed around the people who ride.',priority=false}:{photo?:PhotoName;title?:string;subtitle?:string;priority?:boolean}){const p=photos[photo];return <figure className={'transit-photo photo-'+photo}><img src={p.src} srcSet={photoSources(photo)} sizes="(max-width: 620px) 100vw, (max-width: 1000px) 65vw, 700px" width={p.width} height={p.height} style={{objectPosition:p.position}} alt={p.alt} loading={priority?'eager':'lazy'} fetchPriority={priority?'high':'auto'} decoding="async"/><figcaption><strong>{title}</strong><span>{subtitle}</span></figcaption><a className="photo-credit" href={p.url} target="_blank" rel="noreferrer">Photo: {p.credit}</a></figure>}
