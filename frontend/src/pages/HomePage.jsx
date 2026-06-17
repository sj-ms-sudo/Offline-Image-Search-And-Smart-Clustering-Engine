import { useState } from "react";
import Navbar from "../components/Navbar.jsx"
import Hero from "../components/Hero.jsx"
import CTA from "../components/CTA.jsx"
import StatusCards from "../components/StatusCards.jsx"
import PipeLine from "../components/PipeLine.jsx"
import ImageGrid from "../components/ImageGrid.jsx"
export default function HomePage(){
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