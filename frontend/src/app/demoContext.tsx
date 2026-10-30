import { createContext, useContext, useEffect, useLayoutEffect, useReducer, useState, type ReactNode, type Dispatch } from 'react';
import { demoReducer, safeHydrate, validStoredState } from './demoReducer';
import type { DemoAction, DemoState } from './demoTypes';
interface DemoContextValue { state: DemoState; dispatch: Dispatch<DemoAction>; toast: string; notify:(s:string)=>void; }
const DemoContext=createContext<DemoContextValue | null>(null);
export function DemoProvider({children}:{children:ReactNode}){
  const [state,dispatch]=useReducer(demoReducer,undefined,safeHydrate);
  const [toast,setToast]=useState('');
  useLayoutEffect(()=>{try{localStorage.setItem('naikready-demo-v1',JSON.stringify(state));}catch{}},[state]);
  useEffect(()=>{const sync=(e:StorageEvent)=>{if(e.key!=='naikready-demo-v1'||!e.newValue)return;try{const value:unknown=JSON.parse(e.newValue);if(validStoredState(value))dispatch({type:'RESTORE',state:value});}catch{}};window.addEventListener('storage',sync);return()=>window.removeEventListener('storage',sync);},[]);
  useEffect(()=>{if(!toast)return;const id=window.setTimeout(()=>setToast(''),3500);return()=>window.clearTimeout(id);},[toast]);
  return <DemoContext.Provider value={{state,dispatch,toast,notify:setToast}}>{children}</DemoContext.Provider>;
}
export function useDemo(){const ctx=useContext(DemoContext);if(!ctx)throw new Error('useDemo outside provider');return ctx;}
