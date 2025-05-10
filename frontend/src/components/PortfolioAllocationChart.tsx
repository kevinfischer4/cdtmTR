import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

interface PortfolioAllocationChartProps {
  category: Record<string, number>;
  totalPerformance: number;
}

export function PortfolioAllocationChart({ 
  category, 
  totalPerformance 
}: PortfolioAllocationChartProps) {
  return (
    <div className="h-80 w-full relative">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={Object.entries(category).map(([name, value]) => ({ name, value }))}
            cx="50%"
            cy="50%"
            innerRadius={80}
            outerRadius={120}
            dataKey="value"
            labelLine={false}
            label={({ percent, x, y, midAngle }) => {
              const RADIAN = Math.PI / 180;
              const radius = 140;
              const cx = x;
              const cy = y;
              const sin = Math.sin(-RADIAN * midAngle);
              const cos = Math.cos(-RADIAN * midAngle);
              const sx = cx + (radius + 10) * cos;
              const sy = cy + (radius + 10) * sin;
              
              return (
                <g>
                  <text 
                    x={sx} 
                    y={sy} 
                    fill="#333333" 
                    textAnchor={x > cx ? 'start' : 'end'} 
                    dominantBaseline="central"
                    style={{ fontSize: '12px', fontWeight: '500' }}
                  >
                    {`${(percent * 100).toFixed(0)}%`}
                  </text>
                </g>
              );
            }}
          >
            {Object.entries(category).map(([_], index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={[
                  "#000000", // Black
                  "#333333", // Dark gray
                  "#555555", // Medium gray
                  "#777777", // Gray
                  "#999999", // Light gray
                  "#BBBBBB", // Very light gray
                ][index % 6]} 
              />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value) => `${value}%`}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #eee',
              borderRadius: '4px',
              boxShadow: '0 2px 5px rgba(0,0,0,0.05)',
            }}
            itemStyle={{
              color: '#333',
              fontSize: '12px',
            }}
          />
          <Legend 
            layout="horizontal" 
            verticalAlign="bottom" 
            align="center"
            iconType="circle"
            iconSize={8}
            formatter={(value) => (
              <span style={{ color: '#333', fontSize: '12px', fontWeight: '500' }}>
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
      <div 
        className="absolute inset-0 flex items-center justify-center"
        style={{ pointerEvents: 'none', marginTop: '-24px' }}
      >
        <p 
          className={`text-3xl font-bold ${totalPerformance >= 0 ? 'text-green-500' : 'text-red-500'}`}
        >
          {totalPerformance.toFixed(1)}%
        </p>
      </div>
    </div>
  );
} 