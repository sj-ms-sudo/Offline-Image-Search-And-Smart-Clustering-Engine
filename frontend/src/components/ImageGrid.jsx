import { GalleryHorizontal, Pencil, Check, X, Link, SquareArrowOutUpRight } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
export default function ImageGrid({ refreshSignal }) {
  const [clusters, setClusters] = useState({});
  const [clusterInfo, setClusterInfo] = useState({});
  const [editingCluster, setEditingCluster] = useState(null);
  const [editedName, setEditedName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchClusters() {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/clusters/all`
        );

        const data = await res.json();

        setClusters(data.clusters);
        setClusterInfo(data.cluster_info);
      } catch (error) {
        console.error(error);
      }
    }

    fetchClusters();
  }, [refreshSignal]);

  return (
    <div className="space-y-6 p-8 m-8 max-w-7xl">
      <div>
        <h2 className="flex items-center gap-2 text-xl font-semibold mb-2">
          <GalleryHorizontal className="w-5 h-5" />
          Top Identified Clusters
        </h2>

        <p className="text-zinc-400 text-sm">
          Recent high-confidence matches found in your library.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {Object.entries(clusters).map(([clusterId, images]) => (
          <div
            key={clusterId}
            className="group relative rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden"
          >
            {/* Overlay button */}
            <div className = "relative">
              
            {/* Image Grid */}
            <div className="grid grid-cols-2 gap-1 p-2 transition-all duration-300 blur-none brightness-100 group-hover:blur-xs group-hover:brightness-50">
              {images.slice(0, 4).map((img, index) => {
                const filename = img.split("\\").pop();
                const imageUrl = `${import.meta.env.VITE_BACKEND_URL}/images/${filename}`;

                return (
                  <img
                    key={index}
                    src={imageUrl}
                    alt={`Cluster ${clusterId}`}
                    className="aspect-square object-cover w-full rounded"
                  />
                );
              })}
            </div>
            <div className = "absolute inset-0 items-center justify-center  flex flex-col opacity-0 group-hover:opacity-100 z-20 transition-opacity duration-400">
              <button 
                onClick = {()=>navigate(`/cluster/${clusterId}`)}
                className="flex  gap-4 w-fit bg-blue-600 px-8 py-2 rounded-xl cursor-pointer"
              >
                <SquareArrowOutUpRight className="w-5 h-5"/> <span>Open Cluster</span>
              </button>
              </div>
            </div>

            {/* Footer */}
            <div className="p-4">
              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center gap-2">
                  {editingCluster === clusterId ? (
                    <>
                      <input
                        value={editedName}
                        onChange={(e) => setEditedName(e.target.value)}
                        className="bg-zinc-800 px-2 py-1 rounded text-sm border border-zinc-700 outline-none"
                      />

                      <Check
                        className="w-4 h-4 cursor-pointer hover:text-green-500"
                        onClick={async () => {
                          try {
                            await fetch(
                              `${import.meta.env.VITE_BACKEND_URL}/clusters/editName`,
                              {
                                method: "PATCH",
                                headers: {
                                  "Content-Type": "application/json",
                                },
                                body: JSON.stringify({
                                  cluster_id: Number(clusterId),
                                  name: editedName,
                                }),
                              }
                            );

                            setEditingCluster(null);
                            window.location.reload();
                          } catch (error) {
                            console.error(error);
                          }
                        }}
                      />

                      <X
                        className="w-4 h-4 cursor-pointer hover:text-red-500"
                        onClick={() => {
                          setEditingCluster(null);
                          setEditedName("");
                        }}
                      />
                    </>
                  ) : (
                    <>
                      <h3 className="font-semibold text-lg">
                        {clusterInfo[clusterId]?.name ||
                          `Cluster ${clusterId}`}
                      </h3>

                      <Pencil
                        className="w-4 h-4 cursor-pointer hover:text-blue-400"
                        onClick={() => {
                          setEditingCluster(clusterId);
                          setEditedName(
                            clusterInfo[clusterId]?.name ||
                              `Cluster ${clusterId}`
                          );
                        }}
                      />
                    </>
                  )}
                </div>

                <span className="px-3 py-1 text-xs rounded-full bg-zinc-800">
                  {clusterInfo[clusterId]?.count ?? images.length} photos
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}