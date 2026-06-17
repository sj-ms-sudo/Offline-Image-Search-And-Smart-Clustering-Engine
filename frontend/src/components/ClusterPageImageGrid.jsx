export default function ClusterPageImageGrid({imageArr}){
    const baseURL = `${import.meta.env.VITE_BACKEND_URL}/images/`
    return(
        <section className="bg-[#19191f] text-black h-full m-8">
            <div className="grid grid-cols-4 gap-8 ">
            {imageArr.map((img, index) => {
                const filename = img.split("\\").pop();
                return (
                    <div className = "p-4 m-4 shadow-lg hover:shadow-purple-600/10 hover:scale-105 transition-all ease-in">
                        <img
                        key={index}
                        src={`${baseURL}${filename}`}
                        alt=""
                        className = "w-full aspect-square object-cover rounded-xl border border-zinc-800"
                        />
                    </div>
                    
                );
            })}
            </div>
        </section>
    )
}