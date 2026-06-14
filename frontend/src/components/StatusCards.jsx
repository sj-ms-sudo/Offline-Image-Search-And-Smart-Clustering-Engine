import { useState ,useEffect} from "react"
import { Image, Users , LayoutGrid , Zap } from "lucide-react";
export default function StatusCards(){
    const [imageCount, setImageCount] = useState(0);
    const [faceCount, setFaceCount] = useState(0);
    useEffect(()=>{
        async function fetchImageCount(){
            try{
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/images/count`
                );
                const data = await response.json()
                setImageCount(data.count);
            }catch(error){
                console.error("Failed to fetch image count: ",error)
            }
        }
        async function fetchFaceCount(){
            try{
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/faces/count`
                );
                const data = await response.json()
                setFaceCount(data.count);
            }catch(error){
                console.error("Failed to fetch face count: ",error)
            }
        }
        fetchImageCount();
        fetchFaceCount();
    },[]);
    return(
        <section>
            <div className="flex justify-start p-8 m-8 max-w-5xl gap-8">
                <div>
                    <StatusCard 
                    logo = {<Image className="text-blue-800/80"/>}
                    title = "TOTAL IMAGES"
                    count = {imageCount}
                />
                </div>
                <div>
                    <StatusCard 
                    logo = {<Users/>}
                    title = "FACES DETECTED"
                    count = {faceCount}
                />
                </div>
                <div>
                    <StatusCard 
                    logo = {<LayoutGrid/>}
                    title = "AI CLUSTERS"
                    count = {imageCount}
                />
                </div>
                <div>
                    <StatusCard 
                    logo = {<Zap/>}
                    title = "VECTOR INDEXED"
                    count = {imageCount}
                />
                </div>
            </div>
        </section>
    )
}

function StatusCard({logo,title,count}){
    return (
        <div className="border border-zinc-800 rounded-2xl w-xs h-xl">
            <div className="flex p-4 gap-8">
                <div className="rounded-lg bg-blue-900/30 p-2">
                    {logo}
                </div>
            </div>
            <div className="flex justify-start font-semibold text-xl pl-4 pr-8 text-gray-600">
                {title}
            </div>
            <div className="text-white font-bold text-3xl pl-4 pr-8 mt-2 mb-4">
                {count}
            </div>
        </div>
    )
}