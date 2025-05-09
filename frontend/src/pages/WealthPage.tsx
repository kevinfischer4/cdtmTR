import { Button } from "@/components/ui/button"
import { StockCard } from "@/components/StockCard"

export function WealthPage() {
  return (
    <>
      {/* Portfolio Summary Card */}
      <div className="mb-6">
        <div className="bg-white rounded-xl p-4 shadow-sm">
          <h3 className="text-sm font-medium mb-1 text-muted-foreground">Portfolio</h3>
          <div className="text-2xl font-bold mb-1">€10,432.18</div>
          <div className="text-secondary text-sm">+€243.86 (2.4%)</div>
        </div>
      </div>
      
      {/* Market Section */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-3">Market</h2>
        <div className="space-y-3">
          <StockCard 
            symbol="AAPL.US" 
            name="Apple Inc." 
            price="$195.23" 
            change="+3.45" 
            changePercent="1.80%" 
            isPositive={true} 
          />
          <StockCard 
            symbol="TSLA.US" 
            name="Tesla, Inc." 
            price="$248.29" 
            change="+4.56" 
            changePercent="1.87%" 
            isPositive={true} 
          />
          <StockCard 
            symbol="DAX.DE" 
            name="DAX Index" 
            price="17,842.52" 
            change="+95.33" 
            changePercent="0.54%" 
            isPositive={true} 
          />
          <StockCard 
            symbol="BTC.EUR" 
            name="Bitcoin" 
            price="€51,432.14" 
            change="-632.76" 
            changePercent="1.22%" 
            isPositive={false} 
          />
        </div>
      </div>
      
      {/* Action Buttons */}
      <div>
        <Button className="bg-secondary text-secondary-foreground hover:bg-secondary/90 w-full py-6 text-lg font-medium rounded-xl mb-4">
          Deposit
        </Button>
      </div>
    </>
  )
} 