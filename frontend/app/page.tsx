"use client";

import { useDashboard } from "@/lib/ws";
import TopBar from "@/components/TopBar";
import KPICards from "@/components/KPICards";
import PerformanceChart from "@/components/PerformanceChart";
import PRISMPanel from "@/components/PRISMPanel";
import AgentHierarchy from "@/components/AgentHierarchy";
import PositionsTable from "@/components/PositionsTable";
import ActivityFeed from "@/components/ActivityFeed";
import JANUSSection from "@/components/JANUSSection";

export default function Dashboard() {
  const { state, connected, runAnalysis } = useDashboard();

  return (
    <>
      <TopBar state={state} connected={connected} onRun={runAnalysis} />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-[1fr_1fr_340px] gap-3 md:gap-4 px-3 md:px-6 py-3 md:py-5 max-w-[1600px] mx-auto">
        <KPICards state={state} />

        <PerformanceChart portfolioData={state.portfolio_history} />

        <PRISMPanel state={state} />

        <AgentHierarchy results={state.layer1_results} />

        <PositionsTable positions={state.portfolio.positions} />

        <ActivityFeed logs={state.logs} />

        <JANUSSection />
      </div>
    </>
  );
}
