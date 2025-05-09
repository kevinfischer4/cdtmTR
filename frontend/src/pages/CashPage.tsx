import { Button } from "@/components/ui/button"

export function CashPage() {
  return (
    <>
      {/* Cash Balance */}
      <div className="mb-6">
        <div className="bg-white rounded-xl p-4 shadow-sm">
          <h3 className="text-sm font-medium mb-1 text-muted-foreground">Available Cash</h3>
          <div className="text-2xl font-bold mb-1">€1,243.67</div>
          <div className="text-xs text-muted-foreground">Free, no interest</div>
        </div>
      </div>
      
      {/* Recent Transactions */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-3">Recent Transactions</h2>
        <div className="space-y-4">
          <TransactionItem 
            title="Apple Inc."
            description="Purchase"
            amount="-€142.56"
            date="Today"
            isNegative={true}
          />
          <TransactionItem 
            title="Deposit"
            description="From DE89 1234 5678 9012"
            amount="+€500.00"
            date="Oct 15"
            isNegative={false}
          />
          <TransactionItem 
            title="Tesla, Inc."
            description="Sale"
            amount="+€325.18"
            date="Oct 12"
            isNegative={false}
          />
          <TransactionItem 
            title="Withdrawal"
            description="To DE89 1234 5678 9012"
            amount="-€200.00"
            date="Oct 10"
            isNegative={true}
          />
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="space-y-3">
        <Button className="bg-secondary text-secondary-foreground hover:bg-secondary/90 w-full py-6 text-lg font-medium rounded-xl">
          Deposit
        </Button>
        <Button className="bg-white text-primary border border-border hover:bg-muted w-full py-6 text-lg font-medium rounded-xl">
          Withdraw
        </Button>
      </div>
    </>
  )
}

interface TransactionItemProps {
  title: string;
  description: string;
  amount: string;
  date: string;
  isNegative: boolean;
}

function TransactionItem({ title, description, amount, date, isNegative }: TransactionItemProps) {
  return (
    <div className="flex justify-between items-center py-3 border-b border-border">
      <div>
        <h3 className="font-medium">{title}</h3>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
      <div className="text-right">
        <p className={isNegative ? "text-destructive font-medium" : "text-secondary font-medium"}>
          {amount}
        </p>
        <p className="text-xs text-muted-foreground">{date}</p>
      </div>
    </div>
  )
} 