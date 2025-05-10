import { useState, useMemo } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import { Star, Search } from "lucide-react";
import { Input } from "@/components/ui/input";

export interface ExploreUserData {
  id: string;
  avatarLink: string;
  firstName: string;
  lastName: string;
  keyword1: string;
  keyword2: string;
}

interface UserExplorerProps {
  users: ExploreUserData[];
  onUserSelect?: (user: ExploreUserData) => void;
}

export function UserExplorer({ users, onUserSelect }: UserExplorerProps) {
  const [favorites, setFavorites] = useState<Record<string, boolean>>({});
  const [searchQuery, setSearchQuery] = useState("");

  const toggleFavorite = (userId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavorites(prev => ({
      ...prev,
      [userId]: !prev[userId]
    }));
  };

  const handleUserClick = (user: ExploreUserData) => {
    if (onUserSelect) {
      onUserSelect(user);
    }
  };

  const filteredUsers = useMemo(() => {
    if (!searchQuery.trim()) return users;
    
    const lowerQuery = searchQuery.toLowerCase().trim();
    return users.filter(user => 
      user.firstName.toLowerCase().includes(lowerQuery) ||
      user.lastName.toLowerCase().includes(lowerQuery) ||
      user.keyword1.toLowerCase().includes(lowerQuery) ||
      user.keyword2.toLowerCase().includes(lowerQuery) ||
      `${user.firstName} ${user.lastName}`.toLowerCase().includes(lowerQuery)
    );
  }, [users, searchQuery]);

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="mb-4 relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            placeholder="Search by name or keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 w-full"
          />
          {searchQuery && (
            <button 
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-primary text-sm"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {filteredUsers.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          No users found matching "{searchQuery}"
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {filteredUsers.map((user) => (
            <Card 
              key={user.id}
              className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => handleUserClick(user)}
            >
              <CardContent className="p-4 flex flex-col items-center relative">
                <button
                  onClick={(e) => toggleFavorite(user.id, e)}
                  className="absolute top-2 right-2 text-muted-foreground hover:text-yellow-400 transition-colors"
                  aria-label={favorites[user.id] ? "Remove from favorites" : "Add to favorites"}
                >
                  <Star 
                    size={20} 
                    fill={favorites[user.id] ? "currentColor" : "none"} 
                    className={favorites[user.id] ? "text-yellow-400" : ""}
                  />
                </button>
                
                <Avatar className="h-16 w-16 mb-3">
                  <img src={user.avatarLink} alt={`${user.firstName} ${user.lastName}`} />
                </Avatar>
                
                <h3 className="text-lg font-semibold mb-2 text-center">
                  {user.firstName} {user.lastName}
                </h3>
                
                <div className="flex flex-wrap gap-2 justify-center">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
                    {user.keyword1}
                  </span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
                    {user.keyword2}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
} 