import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { TRTopNav } from "@/components/TRTopNav"
import { WealthPage } from "@/pages/WealthPage"
import { CashPage } from "@/pages/CashPage"
import { CommunityPage } from "@/pages/CommunityPage"

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white pb-8">
        <TRTopNav />
        
        <main className="px-4 pt-4">
          <Routes>
            <Route path="/wealth" element={<WealthPage />} />
            <Route path="/cash" element={<CashPage />} />
            <Route path="/community" element={<CommunityPage />} />
            <Route path="*" element={<Navigate to="/wealth" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
