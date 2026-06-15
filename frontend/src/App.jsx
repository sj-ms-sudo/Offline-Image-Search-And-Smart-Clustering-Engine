import { useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import CTA from "./components/CTA";
import StatusCards from "./components/StatusCards";
import PipeLine from "./components/PipeLine";
import ImageGrid from "./components/ImageGrid";

export default function App(){
  const [refreshSignal, setRefreshSignal] = useState(0);

  const triggerRefresh = () => setRefreshSignal(prev => prev + 1);

  return (
    <main className="min-h-screen w-full bg-black text-white">
      <Navbar/>
      <Hero/>
      <CTA/>
      <StatusCards refreshSignal={refreshSignal}/>
      <PipeLine onTaskComplete={triggerRefresh}/>
      <ImageGrid refreshSignal={refreshSignal}/>
    </main>
  )
}