import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";

import AdminDashboard from "./pages/dashboards/AdminDashboard";
import StaffDashboard from "./pages/dashboards/StaffDashboard";
import SecurityDashboard from "./pages/dashboards/SecurityDashboard";
import HousekeepingDashboard from "./pages/dashboards/HousekeepingDashboard";
import CanteenDashboard from "./pages/dashboards/CanteenDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/staff" element={<StaffDashboard />} />
        <Route path="/security" element={<SecurityDashboard />} />
        <Route path="/housekeeping" element={<HousekeepingDashboard />} />
        <Route path="/canteen" element={<CanteenDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
