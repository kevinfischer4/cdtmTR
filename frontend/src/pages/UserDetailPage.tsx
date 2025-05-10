import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { UserData } from "@/components/UserCarousel";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import { ArrowLeft } from "lucide-react";

export function UserDetailPage() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, you would fetch the user data from an API
    // For now, we'll simulate fetching data with some sample users
    const fetchUser = async () => {
      setLoading(true);
      
      // Sample user data - in a real app, this would come from an API
      const sampleUsers: UserData[] = [
        {
          id: "1",
          profilePicUrl: "https://i.pravatar.cc/300?img=1",
          name: "Emma Johnson",
          text1: "Financial Advisor",
          text2: "Specializes in retirement planning",
        },
        {
          id: "2",
          profilePicUrl: "https://i.pravatar.cc/300?img=2", 
          name: "Michael Chen",
          text1: "Investment Strategist",
          text2: "Focus on sustainable investments",
        },
        {
          id: "3",
          profilePicUrl: "https://i.pravatar.cc/300?img=3",
          name: "Sofia Rodriguez",
          text1: "Wealth Manager",
          text2: "Expert in portfolio diversification",
        },
        {
          id: "4",
          profilePicUrl: "https://i.pravatar.cc/300?img=4",
          name: "James Wilson",
          text1: "Tax Consultant",
          text2: "Specializes in international taxation",
        },
        {
          id: "5",
          profilePicUrl: "https://i.pravatar.cc/300?img=5",
          name: "Aisha Patel",
          text1: "Financial Planner",
          text2: "Expert in family wealth management",
        }
      ];
      
      // Find the user with the matching ID
      const foundUser = sampleUsers.find(u => u.id === userId);
      setUser(foundUser || null);
      setLoading(false);
    };
    
    fetchUser();
  }, [userId]);

  const handleBack = () => {
    navigate(-1); // Go back to the previous page
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8 flex justify-center">
        <p>Loading user details...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="container mx-auto">
        <button 
          onClick={handleBack}
          className="flex items-center text-primary mb-4"
        >
          <ArrowLeft size={16} className="mr-1" /> Back
        </button>
        <Card>
          <CardContent className="py-8">
            <p className="text-center text-muted-foreground">User not found</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4">
      <button 
        onClick={handleBack}
        className="flex items-center text-primary mb-6"
      >
        <ArrowLeft size={16} className="mr-1" /> Back to Community
      </button>
      
      <Card className="max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <Avatar className="h-32 w-32">
              <img src={user.profilePicUrl} alt={user.name} />
            </Avatar>
          </div>
          <CardTitle className="text-2xl">{user.name}</CardTitle>
          <CardDescription className="text-lg">{user.text1}</CardDescription>
        </CardHeader>
        
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Specialty</h3>
              <p>{user.text2}</p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">About</h3>
              <p className="text-muted-foreground">
                This is a placeholder for the user detail page. More information about this community member will be added later.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 