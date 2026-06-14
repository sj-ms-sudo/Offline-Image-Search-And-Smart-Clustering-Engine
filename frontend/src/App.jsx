import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import CTA from "./components/CTA";
import StatusCards from "./components/StatusCards";

export default function App(){
  return (
    <main className="min-h-screen w-full bg-black text-white">
      <Navbar/>
      <Hero/>
      <CTA/>
      <StatusCards/>
    </main>
  )
}