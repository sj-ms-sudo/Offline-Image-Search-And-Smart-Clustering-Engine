import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import ClusterPage from "./pages/ClusterPage";

export default function App() {
  return (
    <BrowserRouter>
      <main className="min-h-screen w-full">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path = "/cluster/:clusterId" element={<ClusterPage/>}/>
        </Routes>
      </main>
    </BrowserRouter>
  );
}