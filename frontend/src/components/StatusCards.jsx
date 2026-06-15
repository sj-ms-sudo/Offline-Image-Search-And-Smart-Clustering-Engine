import { useState ,useEffect} from "react"
import { Image, Users , LayoutGrid , Zap } from "lucide-react";
export default function StatusCards({ refreshSignal }){
    const [imageCount, setImageCount] = useState(0);
    const [faceCount, setFaceCount] = useState(0);
    const [clusterCount,setClusterCount] = useState(0);
    const [indexedVectorCount,setIndexedVectorCount] = useState(0);
    useEffect(()=>{
        async function getStats(){
            try{
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/stats`
                );
                const data = await response.json()
                setImageCount(data.image_count);
                setFaceCount(data.face_count);
                setClusterCount(data.cluster_count);
                setIndexedVectorCount(data.indexed_vector_count);
            }catch(error){
                console.error("Error fetching stats",error)
            }
        }
        getStats();
    },[refreshSignal]);

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
                    logo = {<Users className="text-blue-800/80"/>}
                    title = "FACES DETECTED"
                    count = {faceCount}
                />
                </div>
                <div>
                    <StatusCard 
                    logo = {<LayoutGrid className="text-blue-800/80"/>}
                    title = "AI CLUSTERS"
                    count = {clusterCount}
                />
                </div>
                <div>
                    <StatusCard 
                    logo = {<Zap className="text-blue-800/80"/>}
                    title = "VECTOR INDEXED"
                    count = {indexedVectorCount}
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