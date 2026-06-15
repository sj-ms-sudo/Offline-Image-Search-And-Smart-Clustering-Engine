import {ArrowRight, Cpu, Database, File, Search, Fingerprint, SquareStackIcon, Trash2} from "lucide-react"
import { useEffect, useState } from "react"
import { useRef } from "react"
export default function PipeLine({ onTaskComplete }){
    const [jobStatusQueue,setJobStatusQueue] = useState("IDLE")
    const [uploadCount, setUploadCount] = useState(0);
    const [totalToUpload, setTotalToUpload] = useState(0);
    const [fileUploadStatus,setFileUploadStatus] = useState("idle")
    const [databaseSyncStatus,setDatabaseSyncStatus] = useState("idle")
    const [FAISSIndexingStatus,setFAISSIndexingStatus] = useState("idle")
    const [embeddingStatus, setEmbeddingStatus] = useState("idle")
    const [clusterStatus,setClusterStatus] = useState("idle")
    const [deleteStatus, setDeleteStatus] = useState("idle")
    
    const [fileUploadMessage, setFileUploadMessage] = useState("")
    const [databaseSyncMessage,setDatabaseSyncMessage]= useState("") 
    const [FAISSIndexingMessage, setFAISSIndexingMessage] = useState("")
    const [embeddingMessage, setEmbeddingMessage] = useState("")
    const [embeddingProgress, setEmbeddingProgress] = useState({ current: 0, total: 0 })
    const [deleteMessage, setDeleteMessage] = useState("")
    const [clusterMessage,setClusterMessage] = useState("")
    const [clusterProgress,setClusterProgress] = useState({current:0,total:0})
    const fileInputRef = useRef(null);

    const handleFAISSIndexingClick = async () => {
        setJobStatusQueue("INDEXING...");
        setFAISSIndexingStatus("running")
        try{
            const res = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/indexing`,
                {
                    method:"POST",
                }
            );
            const data = await res.json();
            
            if (!res.ok){
                throw new Error(data.message)
            }
            console.log(data.message);
            onTaskComplete?.();
            setFAISSIndexingMessage(data.message)
            setFAISSIndexingStatus("idle")
        }catch(error){
            console.log(error);
            setFAISSIndexingMessage(error.message);
            setFAISSIndexingStatus("error")
        }
        setJobStatusQueue("IDLE");
    }
    const handleSync = async()=>{
        setJobStatusQueue("SYNCING...");
        setDatabaseSyncStatus("running")
        try{
            const res = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/database/sync`,
                {
                    method:"POST",
                }
            );
            const data = await res.json();
            
            if (!res.ok){
                throw new Error(data.message);
            }
            console.log(data.message);
            onTaskComplete?.();
            setDatabaseSyncMessage(data.message)
            setDatabaseSyncStatus("idle")
        }catch(error){
            console.log(error);
            setDatabaseSyncMessage(error.message);
            setDatabaseSyncStatus("error")
        }
        setJobStatusQueue("IDLE");
    }
    const handleFileUpload = async (event) => {
        setFileUploadStatus("running")
        const files = Array.from(event.target.files);
        if (!files || files.length === 0 || jobStatusQueue !== "IDLE") return;

        setTotalToUpload(files.length);
        setUploadCount(0);
        setJobStatusQueue("UPLOADING...");

        for (let i = 0; i < files.length; i++) {
            const formData = new FormData();
            formData.append("files", files[i]);

            try {
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}/upload`,
                    {
                        method: "POST",
                        body: formData,
                    }
                );
                
                if (!response.ok) throw new Error("Upload failed");
                setUploadCount(i + 1);
            } catch (error) {
                console.error("File upload failed", error);
                setJobStatusQueue("ERROR");
                setFileUploadStatus("error");
                return;
            }
        }
        setFileUploadStatus("idle")
        setJobStatusQueue("IDLE");
        setFileUploadMessage("File Upload Successful")
        onTaskComplete?.();
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    const handleCreateEmbeddings = async () => {
        setEmbeddingStatus("running");
        setJobStatusQueue("EMBEDDING...");
        setEmbeddingMessage("");
        
        try {
            const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/embeddings`, {
                method: "POST",
            });
            
            if (!res.ok) throw new Error("Failed to start embedding process");
            const pollInterval = setInterval(async () => {
                try {
                    const statusRes = await fetch(`${import.meta.env.VITE_BACKEND_URL}/embeddings/status`);
                    const statusData = await statusRes.json();
                    const { current, total, status } = statusData.progress;

                    setEmbeddingProgress({ current, total });

                    if (status === "completed") {
                        clearInterval(pollInterval);
                        setEmbeddingStatus("idle");
                        setJobStatusQueue("IDLE");
                        setEmbeddingMessage("Face embeddings generated successfully");
                        onTaskComplete?.();
                    }
                } catch (e) {
                    console.error("Polling error", e);
                }
            }, 1000);
        } catch (error) {
            setEmbeddingStatus("error");
            setEmbeddingMessage(error.message);
            setJobStatusQueue("IDLE");
        }
    };

    const handleCreateCluster = async() =>{
        setClusterStatus("running");
        setJobStatusQueue("CLUSTERING...");
        setClusterMessage("");
        try{
            const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/clusters`,{
                method:"POST",
            });
            if(!res.ok) throw new Error("Failed to start clustering process");
            const pollInterval = setInterval(async()=>{
                try{
                    const statusRes = await fetch(`${import.meta.env.VITE_BACKEND_URL}/clusters/status`);
                    const statusData = await statusRes.json();
                    const {current,total,status} = statusData.progress;
                    setClusterProgress({current,total});
                    if(status === "completed"){
                        clearInterval(pollInterval);
                        setClusterStatus("idle");
                        setJobStatusQueue("IDLE");
                        setClusterMessage("Face clusters generated successfully");
                        onTaskComplete?.();
                    }
                }catch(e){
                    console.error("Polling error",e);
                }
            },1000);
        }catch(error){
            setClusterStatus("error");
            setClusterMessage(error.message);
            setJobStatusQueue("IDLE");      
                }
        }
    
    const handleDeleteAllData = async () => {
        if (!window.confirm("Are you sure you want to delete all system data? This action cannot be undone.")) {
            return;
        }

        setDeleteStatus("running");
        setJobStatusQueue("DELETING DATA...");
        setDeleteMessage("");

        try {
            const res = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}/files`,
                {
                    method: "DELETE",
                }
            );
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Failed to delete data");
            setDeleteMessage(data.message);
            setDeleteStatus("idle");
            onTaskComplete?.(); // Refresh stats after deletion
        } catch (error) {
            setDeleteMessage(error.message);
            setDeleteStatus("error");
        }
        setJobStatusQueue("IDLE");
    };

    return(
        <section>
            <div className=" p-8 m-8 max-w-7xl gap-8">
                <div className="flex items-center w-full gap-8">
                    <div className="text-violet-800 text-xl font-bold">
                        <Cpu className="text-3xl size-11"/>
                    </div>
                    <div>
                        <h1 className="font-bold text-4xl text-gray-50/90">
                            Processing Pipeline
                        </h1>
                    </div>
                    <div className="ml-auto flex flex-col items-end gap-2">
                        <p className={`font-medium ${jobStatusQueue === "IDLE" ? "text-zinc-400" : "text-green-400"}`}>
                            {jobStatusQueue === "UPLOADING..." 
                                ? `UPLOADING: ${uploadCount} / ${totalToUpload}` 
                                : jobStatusQueue === "EMBEDDING..."
                                ? `EMBEDDING: ${embeddingProgress.current} / ${embeddingProgress.current}`
                                : `JOB QUEUE STATUS: ${jobStatusQueue}`}
                        </p>
                        {jobStatusQueue === "UPLOADING..." && (
                            <div className="w-48 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                                <div 
                                    className="h-full bg-violet-600 transition-all duration-300 ease-out" 
                                    style={{ width: `${(uploadCount / totalToUpload) * 100}%` }}
                                />
                            </div>
                        )}
                    </div>
                </div>
                <div className="grid grid-cols-2 gap-8 ">
                    <PipelineCards 
                        icon = {<File className="text-violet-800"/>}
                        title= "File Uploads"
                        description = "Add new photos or folders from this device into your library for processing"
                        onClick={() => fileInputRef.current?.click()}
                        status={fileUploadStatus}
                        message={fileUploadMessage}
                    />
                    <PipelineCards
                        icon={<Database className="text-violet-800"/>}
                        title="SQLite Sync"
                        description="Synchronize local file metadata with the high-perfomance relational database."
                        onClick={handleSync}
                        status={databaseSyncStatus}
                        message={databaseSyncMessage}
                    />
                    <PipelineCards
                        icon={<Search className="text-violet-800"/>}
                        title="FAISS Indexing"
                        description = "Built a highly optimized vector search index for sub millisecond similarity lookups."
                        onClick={handleFAISSIndexingClick}
                        status = {FAISSIndexingStatus}
                        message = {FAISSIndexingMessage}
                    />
                    <PipelineCards
                        icon={<Fingerprint className="text-violet-800"/>}
                        title="Feature Extraction"
                        description="Generate 512-dimensional vector embeddings using the local ResNet model."
                        onClick={handleCreateEmbeddings}
                        status={embeddingStatus}
                        message={embeddingMessage}
                        progress={embeddingProgress}
                    />
                    <PipelineCards
                        icon={<SquareStackIcon className="text-violet-800"/>}
                        title="DBSCAN Clustering"
                        description = "Execute intelligent grouping using density-based algorithms on the embedding space."
                        onClick={handleCreateCluster}
                        status={clusterStatus}
                        message={clusterMessage}
                        progress={clusterProgress}
                    />
                    <PipelineCards
                        icon={<Trash2 className="text-violet-800"/>}
                        title="Clear All Data"
                        description="Delete all uploaded photos, generated embeddings, FAISS index, and database entries."
                        onClick={handleDeleteAllData}
                        status={deleteStatus}
                        message={deleteMessage}
                    />
                
                </div>
                <input 
                    type="file"
                    accept="image/*"
                    multiple
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    className="hidden"
                />
                
            </div>
        </section>    
    )
}
const statusStyles = {
    idle: "bg-zinc-800/70 text-zinc-300 border border-zinc-700",
    running: "bg-green-500/10 text-green-400 border border-green-500/30",
    error: "bg-red-500/10 text-red-400 border border-red-500/30",
};
function PipelineCards({icon,title,description,onClick,status,message,progress}){
    return(
        <div className = "border border-zinc-800 rounded-2xl p-8 mt-8">
            <div className="flex justify-between items-center gap-4">
                <div className = "bg-violet-900/20 rounded-2xl p-2 w-12 h-12 items-center justify-center flex">
                    {icon}
                </div>
                <div
    className={`px-3 py-1 rounded-full text-xs font-semibold ${statusStyles[status]}`}>
                    {status}
                </div>
            </div>
            
            <div className="mt-4 font-bold text-2xl font-white">
                <h1>{title}</h1>
            </div>
            <div className="mt-3 font-semibold text-white/60">
                <p >{description}</p>
            </div>

            {status === "running" && progress && progress.total > 0 && (
                <div className="mt-6">
                    <div className="flex justify-between text-xs text-zinc-400 mb-1.5 font-medium">
                        <span>Processing vectors...</span>
                        <span>{Math.round((progress.current / progress.total) * 100)}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-violet-600 transition-all duration-500 ease-out" 
                            style={{ width: `${(progress.current / progress.total) * 100}%` }}
                        />
                    </div>
                </div>
            )}

            <div className="mt-6 flex items-center text-violet-800/70 font-bold cursor-pointer hover:text-violet-800 hover:translate-x-0.5  transition-all ease-in duration-500" onClick={onClick}>
                <p className="flex items-center gap-2 hover:gap-3">Launch Module <ArrowRight className="transition-transform duration-500 group-hover:translate-x-2"/></p> 
            </div>
            <div>
                {message && (
                    <p className = "mt-3 text-sm text-green-400">{message}</p>
                )}
            </div>
        </div>
    )
}