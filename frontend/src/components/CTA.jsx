import { Shield, Zap } from "lucide-react";

export default function CTA(){
    return(
         <section>
        <div className="flex justify-start p-8 m-8 max-w-4xl gap-8">
            <div >
                <button className="flex bg-gradient-to-r from-blue-500 via blue-800 to-violet-500 rounded-xl p-4 w-60">
                    <Zap className="text-white"></Zap>
                    <p className="text-black pl-4 font-bold ">Start Processing</p>
                </button>
            </div>
            <div >
                <button className="border border-zinc-500 rounded-xl p-4 w-60">
                    <p className="text-white font-bold ">View Documentation</p>
                </button>
            </div>
        </div>
        <div className="flex justify-start p-8 m-8 max-w-7xl gap-2 border border-zinc-800 rounded-xl bg-slate-900/20">
            <div>
                <Shield className="text-gray-500"/>
            </div>
            <div>
                <p className="text-gray-500">
                    In this web version, your images are uploaded to our servers for processing - we never use them to train AI models and they are deleted after processing.
                    For maximum privacy, with all your processing kept fully on your device, we recomend using the desktop application.
                </p>
            </div>
        </div>
    </section>
    )
   
}