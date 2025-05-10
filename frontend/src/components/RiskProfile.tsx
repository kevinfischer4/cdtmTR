import React, { useState } from "react";
import { Info } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface RiskProfileProps {
  riskRatio: number;
  riskText: string;
}

export function RiskProfile({ riskRatio: sharpRatio, riskText }: RiskProfileProps) {
  const [tooltipOpen, setTooltipOpen] = useState(false);

  // Determine risk level based on the sharpe ratio value
  const getRiskLevel = (ratio: number): string => {
    if (ratio < 0.5) return "Low Risk/Low Reward";
    if (ratio < 2.0) return "Good";
    if (ratio < 3.0) return "Very Good";
    if (ratio < 4.0) return "Outstanding";
    return "Outstanding";
  };

  // Get appropriate color based on risk level
  const getRiskColor = (ratio: number): string => {
    if (ratio < 0.5) return "bg-red-500";
    if (ratio < 2.0) return "bg-orange-500";
    if (ratio < 3.0) return "bg-yellow-500";
    return "bg-green-500";
  };

  const riskLevel = getRiskLevel(sharpRatio);
  const riskColor = getRiskColor(sharpRatio);

  // Calculate width as percentage of max (4.0)
  const barWidth = Math.min(100, (sharpRatio / 4.0) * 100);

  const handleTooltipClick = () => {
    setTooltipOpen(!tooltipOpen);
  };

  return (
    <div className="bg-slate-50 p-4 rounded-lg">
      <div className="flex items-center gap-3 mb-2">
        <div className="flex items-center gap-1.5">
          <p className="text-sm text-muted-foreground">Sharp Ratio</p>
          <TooltipProvider>
            <Tooltip open={tooltipOpen} onOpenChange={setTooltipOpen}>
              <TooltipTrigger asChild>
                <button 
                  className="inline-flex touch-manipulation" 
                  onClick={handleTooltipClick}
                  aria-label="Information about Sharp Ratio"
                >
                  <Info size={14} className="text-muted-foreground" />
                </button>
              </TooltipTrigger>
              <TooltipContent className="max-w-xs">
                <p>The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, after adjusting for its risk. It represents the additional amount of return that an investor receives per unit of increase in risk. Higher values (above 1.0) indicate better risk-adjusted returns.</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
          <div 
            className={`h-full ${riskColor} rounded-full`} 
            style={{ width: `${barWidth}%` }}
          ></div>
        </div>
        <div className="flex items-center gap-1.5">
          <p className="text-sm font-medium">{sharpRatio.toFixed(2)}</p>
          <span className="text-xs px-1.5 py-0.5 rounded bg-slate-200">{riskLevel}</span>
        </div>
      </div>
      <p className="text-sm">{riskText}</p>
    </div>
  );
} 