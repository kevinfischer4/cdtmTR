interface StockCardProps {
  symbol: string
  name: string
  price: string
  change: string
  changePercent: string
  isPositive: boolean
}

export function StockCard({ symbol, name, price, change, changePercent, isPositive }: StockCardProps) {
  return (
    <div className="bg-white py-4 flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
      <div className="flex-1">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center mr-3">
            <span className="font-semibold text-xs">{symbol.slice(0, 2)}</span>
          </div>
          <div>
            <h3 className="font-medium text-base">{name}</h3>
            <p className="text-xs text-muted-foreground">{symbol}</p>
          </div>
        </div>
      </div>
      
      <div className="text-right">
        <p className="font-bold text-base">{price}</p>
        <p className={`text-sm ${isPositive ? 'text-secondary' : 'text-destructive'}`}>
          {change} ({changePercent})
        </p>
      </div>
    </div>
  )
} 