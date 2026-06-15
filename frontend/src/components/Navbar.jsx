import { Wallpaper } from "lucide-react";

export default function Navbar(){
    return (
        <section className="bg-black text-white">
            <div className="flex justify-between items-center p-8">
                <div className="flex items-center justify-start gap-8">
                    <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-xl shadow-lg shadow-blue-600/20">
                        <Wallpaper className="text-white w-6 h-6" strokeWidth={2.5} />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight text-blue-800">Face Clustering Engine</h1>
                    <div className="h-5 w-px bg-zinc-800" />
                    <span className="text-zinc-400 font-medium">Dashboard</span>
                </div>
                <div className="flex items-center">
                    <div className="flex items-center gap-3 px-3 py-1.5 rounded-md border border-green-500/30 bg-green-500/10 shadow-[0_0_15px_rgba(34,197,94,0.15)]">
                        <div className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500 shadow-[0_0_5px_rgba(34,197,94,1)]"></span>
                        </div>
                        <span className="text-[11px] font-bold text-green-400 uppercase tracking-widest">
                            Local AI processing
                        </span>
                    </div>
                </div>
            </div>
            <div className = "h-px w-full bg-zinc-800"></div>
        </section>
    )
}