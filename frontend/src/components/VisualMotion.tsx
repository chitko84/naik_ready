import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
/** Progressive enhancement: content stays visible without observers or motion. */
export default function VisualMotion(){const {pathname}=useLocation();useEffect(()=>{
 if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const seen=new WeakSet<Element>();
 const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){entry.target.classList.add('visual-reveal');observer.unobserve(entry.target)}},{threshold:.06});
 const watch=()=>document.querySelectorAll('.landing-section,.landing-cta,.page-titlebar,.role-card,.kpi-card,.panel,.scene-status-panel,.transit-photo').forEach(el=>{if(seen.has(el))return;seen.add(el);observer.observe(el)});
 watch();const mutations=new MutationObserver(watch);mutations.observe(document.body,{childList:true,subtree:true});return()=>{observer.disconnect();mutations.disconnect()};
 },[pathname]);return null}
