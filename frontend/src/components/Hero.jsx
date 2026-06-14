export default function Hero(){
    return(
        <section>
            <div className = "flex items-center p-8 m-8 max-w-4xl">
                <div className = "flex items-center gap-3 px-3 py-1.5 rounded-lg border border-violet-500/30 bg-violet-500/10 shadow-[0_0_15px_rgba(142,94,255,0.15)]">
                    <span className="text-md font-bold text-violet-400 uppercase tracking-widest">
                        Local AI Engine v0.8
                    </span>
                </div>
            </div>
            <div className="p-8 m-8">
                <h1 className="text-7xl font-bold tracking-tight leading-[1.15]">Organize your <br></br>
                    <span className="bg-gradient-to-r from-blue-500 via-blue-800 to-violet-500 bg-clip-text text-transparent "> unstructured photos </span>
                    with <br></br>local intelligence.    
                </h1>    
            </div>
            <div className="p-8 m-8 max-w-4xl">
                <p className="text-lg font-medium leading-8">Fast, private, and powerful face recognition. Process tens of thousands of images locally on your machine
                    using advanced vector search and clustering algorithms.
                </p>    
            </div>   
        </section>
    )
}