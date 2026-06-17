import { useNavigate } from "react-router-dom"
import { ChevronLeft, Image } from "lucide-react"
export default function ({name , count}){
    const navigate = useNavigate();
    return (
        <section>
            {/* Container div */}
            <div className = "flex flex-col m-8 ">
                {/* div for button */}
                <div>
                    {/* to home button */}
                    <button
                        onClick={() => navigate("/")}
                        className = "flex items-center gap-2 px-4 py-2 rounded-lg hover:text-zinc-200 transition-colors duration-300"
                    >
                        <ChevronLeft className="w-5 h-5" /> Back to Home
                    </button>
                </div>

                <div className = "flex gap-32 items-center justify-start mt-8 ">
                    <div >
                        <h1 className = "font-bold text-5xl leading-tight text-white">{name}</h1>
                    </div>
                    <div>
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/10 border border-white/30 rounded-lg mt-4">
                            <Image className="w-5 h-5" />
                                <span>TOTAL : {count}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div className = "bg-zinc-800 w-full h-px">
            </div>
        </section>
    )
}