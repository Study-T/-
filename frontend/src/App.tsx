import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { lazy, Suspense } from "react";
import Layout from "./components/Layout";

const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/Login"));
const AvatarCreate = lazy(() => import("./pages/AvatarCreate"));
const AvatarDetail = lazy(() => import("./pages/AvatarDetail"));
const TryOn = lazy(() => import("./pages/TryOn"));
const History = lazy(() => import("./pages/History"));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div className="loading-screen">Loading...</div>}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<Layout />}>
            <Route path="/home" element={<Home />} />
            <Route path="/avatar/create" element={<AvatarCreate />} />
            <Route path="/avatar/:id" element={<AvatarDetail />} />
            <Route path="/tryon/:garmentId" element={<TryOn />} />
            <Route path="/history" element={<History />} />
          </Route>
          <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default App;
