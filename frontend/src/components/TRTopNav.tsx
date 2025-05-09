import { NavLink, useLocation } from "react-router-dom"

const NAV_ITEMS = [
  { key: "wealth", label: "Wealth", path: "/wealth" },
  { key: "cash", label: "Cash", path: "/cash" },
  { key: "community", label: "Community", path: "/community" },
]

export function TRTopNav() {
  const location = useLocation()
  
  return (
    <div className="sticky top-0 bg-white z-10">
      <div className="h-16 flex items-center px-4">
        <div className="flex space-x-5">
          {NAV_ITEMS.map(item => {
            const isActive = location.pathname === item.path
            return (
              <NavLink
                key={item.key}
                to={item.path}
                className={`text-xl ${
                  isActive
                    ? "font-bold text-black" 
                    : "font-medium text-muted-foreground"
                }`}
              >
                {item.label}
              </NavLink>
            )
          })}
        </div>
      </div>
    </div>
  )
} 