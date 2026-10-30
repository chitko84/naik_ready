import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useEffect, lazy, Suspense } from 'react';
import { AppHeader, Footer, MobileNav } from '../components/UI';
import { useDemo, DemoProvider } from './demoContext';
import Welcome from '../pages/Welcome';
import {PassengerHome, RequestAssistance, PassengerStatus} from '../pages/Passenger';
import Driver from '../pages/Driver';
const Operator=lazy(()=>import('../pages/Operator'));
const Experience=lazy(()=>import('../pages/Experience'));
const ScenarioLab=lazy(()=>import('../pages/ScenarioLab'));
const Activity=lazy(()=>import('../pages/Activity'));
import { CheckCircle2 } from 'lucide-react';
function PageReset(){const {pathname}=useLocation();useEffect(()=>{window.scrollTo({top:0,behavior:'instant'});},[pathname]);return null}
function AppPages(){const{toast}=useDemo();return <><PageReset/><AppHeader/><Suspense fallback={<div className="page-loading" role="status">Loading your workspace…</div>}><Routes><Route path="/" element={<Welcome/>}/><Route path="/passenger" element={<PassengerHome/>}/><Route path="/passenger/request" element={<RequestAssistance/>}/><Route path="/passenger/status" element={<PassengerStatus/>}/><Route path="/driver" element={<Driver/>}/><Route path="/operator" element={<Operator/>}/><Route path="/experience" element={<Experience/>}/><Route path="/demo" element={<ScenarioLab/>}/><Route path="*" element={<Navigate to="/" replace/>}/><Route path="/activity" element={<Activity/>}/></Routes></Suspense><Footer/><MobileNav/>{toast&&<div className="toast" role="status" aria-live="polite"><CheckCircle2 size={19}/>{toast}</div>}</>}
export default function App(){return <BrowserRouter><DemoProvider><AppPages/></DemoProvider></BrowserRouter>}
