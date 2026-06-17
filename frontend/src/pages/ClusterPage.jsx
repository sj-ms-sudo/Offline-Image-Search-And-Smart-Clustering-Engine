import { useState ,useEffect} from "react";
import ClusterPageHeader from "../components/ClusterPageHeader";
import ClusterPageImageGrid from "../components/ClusterPageImageGrid";
import { useParams } from "react-router-dom";
export default function ClusterPage(){
    const { clusterId } = useParams();
    const [name,setName] = useState("");
    const [count,setCount] = useState(0);
    const [images,setImages] = useState([])
    useEffect(()=>{
        async function fetchCluster(){
            try{
                const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/clusters/${clusterId}`)
                const data = await res.json();
                setName(data.cluster_name)
                setCount(data.cluster_count)
                setImages(data.image_paths)
            }catch(error){
                console.error(error);
            }
        }
        if(clusterId){
            fetchCluster()
        }
    }, [clusterId])
    return (
        <section className="bg-[#19191f] text-white">
            <ClusterPageHeader name={name} count={count}/>
            <ClusterPageImageGrid imageArr={images}/>
        </section>
    )
}