import { GalleryHorizontal } from "lucide-react";
import { useEffect,useState } from "react";
export default function ImageGrid({ refreshSignal }){
    const [clusters,setClusters] = useState({});
    useEffect(()=>{
        async function fetchClusters(){
            try{
                const res = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/clusters/all`)
                const data = await res.json();
                setClusters(data);
            }catch(error){
                console.error(error)
            }
    }
    fetchClusters();
},[refreshSignal])
    return(
        <div className = "p-8">
            <div className = "flex items-center gap-3 mb-2">
                <GalleryHorizontal className="h-6 w-6 text-blue-500"/>
                <h1 className = "text-4xl font-bold">
                    Top Identified Clusters
                </h1>
            </div>
            <p className = "text-zinc-400 mb-8">
                Recent high-confidence matches found in your library.
            </p>
            <div className = "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                {Object.entries(clusters).map(([clusterId,images])=>(
                    <div
                        key={clusterId}
                        className = "bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden"
                    >
                        <div className="grid grid-cols-2 gap-1 p-1">
              {images.slice(0, 4).map((img, index) => {
                // Extract the filename from the local path
                // This assumes Windows-style paths (C:\...)
                // You might need to adjust this if your backend provides Unix-style paths or relative paths.
                const filename = img.split('\\').pop();
                // Construct the full URL using your backend's base URL and an image-serving endpoint
                const imageUrl = `${import.meta.env.VITE_BACKEND_URL}/images/${filename}`;
                return (
                  <img
                    key={index}
                    src={imageUrl} // Use the constructed URL
                    alt={`Cluster ${clusterId}`}
                    className="aspect-square object-cover w-full rounded"
                  />
                );
              })}
            </div>

            {/* Footer */}
            <div className="p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="font-semibold text-lg">
                  Cluster {clusterId}
                </h3>

                <span className="px-3 py-1 text-xs rounded-full bg-zinc-800">
                  {images.length} photos
                </span>
              </div>

              <div className="w-full h-2 bg-zinc-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500"
                  style={{ width: "95%" }}
                />
              </div>

              <div className="text-right mt-2 text-sm text-zinc-400">
                95% match
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}