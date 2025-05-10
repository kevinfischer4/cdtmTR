import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { UserData } from "@/components/UserCarousel";
import { ExploreUserData } from "@/components/UserExplorer";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import { ArrowLeft } from "lucide-react";
import { PortfolioAllocationChart } from "@/components/PortfolioAllocationChart";
import { RiskProfile } from "@/components/RiskProfile";

// Extended user data interface that includes investment details
interface ExtendedUserData extends UserData {
  summary: string;
  sharpRatio: number;
  total_performance: number;
  riskText: string;
  category: Record<string, number>;
}

// Extended explore user data interface
interface ExtendedExploreUserData extends ExploreUserData {
  summary: string;
  sharpRatio: number;
  total_performance: number;
  riskText: string;
  category: Record<string, number>;
}

// Union type for both types of user data
type AnyUserData = ExtendedUserData | ExtendedExploreUserData;

export function UserDetailPage() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<AnyUserData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, you would fetch the user data from an API
    // For now, we'll simulate fetching data with some sample users
    const fetchUser = async () => {
      setLoading(true);
      
      // Sample user data - in a real app, this would come from an API
      const sampleUsers: ExtendedUserData[] = [
        {
          id: "1",
          profilePicUrl: "https://i.pravatar.cc/300?img=1",
          name: "Emma Johnson",
          text1: "Financial Advisor",
          text2: "Specializes in retirement planning",
          summary: "Conservative investor with focus on long-term growth",
          sharpRatio: 0.85,
          total_performance: 8.2,
          riskText: "Moderate risk profile with balanced portfolio allocation",
          category: {
            "Stocks": 40,
            "Bonds": 35,
            "Real Estate": 15,
            "Cash": 10
          }
        },
        {
          id: "2",
          profilePicUrl: "https://i.pravatar.cc/300?img=2", 
          name: "Michael Chen",
          text1: "Investment Strategist",
          text2: "Focus on sustainable investments",
          summary: "Aggressive investor targeting high-growth sectors",
          sharpRatio: 2.4,
          total_performance: 12.5,
          riskText: "Higher risk tolerance with technology-focused portfolio",
          category: {
            "Tech Stocks": 60,
            "Green Energy": 20,
            "Bonds": 10,
            "Cryptocurrencies": 10
          }
        },
        {
          id: "3",
          profilePicUrl: "https://i.pravatar.cc/300?img=3",
          name: "Sofia Rodriguez",
          text1: "Wealth Manager",
          text2: "Expert in portfolio diversification",
          summary: "Balanced approach with international exposure",
          sharpRatio: 1.75,
          total_performance: 9.8,
          riskText: "Moderate-high risk with geographic diversification",
          category: {
            "US Stocks": 30,
            "International Equities": 30,
            "Corporate Bonds": 25,
            "Commodities": 15
          }
        },
        {
          id: "4",
          profilePicUrl: "https://i.pravatar.cc/300?img=4",
          name: "James Wilson",
          text1: "Tax Consultant",
          text2: "Specializes in international taxation",
          summary: "Tax-efficient portfolio with focus on income",
          sharpRatio: 0.45,
          total_performance: 6.3,
          riskText: "Lower risk profile emphasizing dividend stocks and municipal bonds",
          category: {
            "Dividend Stocks": 35,
            "Municipal Bonds": 40,
            "REITs": 15,
            "Treasury Bills": 10
          }
        },
        {
          id: "5",
          profilePicUrl: "https://i.pravatar.cc/300?img=5",
          name: "Aisha Patel",
          text1: "Financial Planner",
          text2: "Expert in family wealth management",
          summary: "Growth-oriented approach for generational wealth",
          sharpRatio: 3.2,
          total_performance: -10.2,
          riskText: "High risk approach with focus on long-term appreciation",
          category: {
            "Growth Stocks": 45,
            "Index Funds": 25,
            "Corporate Bonds": 20,
            "Alternative Investments": 10
          }
        }
      ];
      
      // Sample explorer user data
      const sampleExploreUsers: ExtendedExploreUserData[] = [
        {
          id: "101",
          avatarLink: "https://i.pravatar.cc/300?img=11",
          firstName: "David",
          lastName: "Garcia",
          keyword1: "Crypto",
          keyword2: "Tech Stocks",
          summary: "Tech enthusiast with focus on cryptocurrency investments",
          sharpRatio: 3.1,
          total_performance: 15.7,
          riskText: "High risk profile with significant crypto exposure",
          category: {
            "Bitcoin": 30,
            "Ethereum": 20,
            "Tech Stocks": 40,
            "Cash": 10
          }
        },
        {
          id: "102",
          avatarLink: "https://i.pravatar.cc/300?img=12",
          firstName: "Sarah",
          lastName: "Miller",
          keyword1: "ESG",
          keyword2: "Green Energy",
          summary: "Environmental advocate focusing on sustainable investments",
          sharpRatio: 1.4,
          total_performance: 7.8,
          riskText: "Moderate risk with ESG-focused portfolio",
          category: {
            "Renewable Energy": 45,
            "Sustainable ETFs": 30,
            "Green Bonds": 20,
            "Water Technology": 5
          }
        },
        {
          id: "103",
          avatarLink: "https://i.pravatar.cc/300?img=13",
          firstName: "Robert",
          lastName: "Kim",
          keyword1: "Real Estate",
          keyword2: "Bonds",
          summary: "Conservative investor with focus on steady income",
          sharpRatio: 0.8,
          total_performance: 5.3,
          riskText: "Low-moderate risk with focus on income-generating assets",
          category: {
            "REITs": 40,
            "Municipal Bonds": 30,
            "Corporate Bonds": 20,
            "CDs": 10
          }
        },
        {
          id: "104",
          avatarLink: "https://i.pravatar.cc/300?img=14",
          firstName: "Jennifer",
          lastName: "Thompson",
          keyword1: "Startups",
          keyword2: "Angel Investing",
          summary: "Venture capital enthusiast with focus on early-stage startups",
          sharpRatio: 4.2,
          total_performance: -5.7,
          riskText: "Very high risk with significant allocation to private companies",
          category: {
            "Angel Investments": 50,
            "Tech Startups": 30,
            "VC Funds": 15,
            "Public Equities": 5
          }
        },
        {
          id: "105",
          avatarLink: "https://i.pravatar.cc/300?img=15",
          firstName: "Ahmed",
          lastName: "Hassan",
          keyword1: "Commodities",
          keyword2: "Forex",
          summary: "Alternative investment specialist with global perspective",
          sharpRatio: 2.1,
          total_performance: 9.4,
          riskText: "High risk with focus on market fluctuations",
          category: {
            "Gold": 25,
            "Oil & Gas": 20,
            "Currency Pairs": 40,
            "Agricultural Commodities": 15
          }
        },
        {
          id: "106",
          avatarLink: "https://i.pravatar.cc/300?img=16",
          firstName: "Lisa",
          lastName: "Wong",
          keyword1: "Dividends",
          keyword2: "Value Investing",
          summary: "Long-term value investor focusing on reliable income",
          sharpRatio: 0.95,
          total_performance: 6.8,
          riskText: "Low risk with focus on established companies",
          category: {
            "Dividend Aristocrats": 45,
            "Blue Chip Stocks": 30,
            "Preferred Shares": 15,
            "Value ETFs": 10
          }
        }
      ];
      
      // Find the user with the matching ID from either dataset
      const foundUser = sampleUsers.find(u => u.id === userId) || 
                       sampleExploreUsers.find(u => u.id === userId);
      
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

  // Determine if this is a carousel user or an explore user
  const isExploreUser = 'firstName' in user;

  return (
    <div className="container mx-auto px-4">
      <button 
        onClick={handleBack}
        className="flex items-center text-primary mb-6"
      >
        <ArrowLeft size={16} className="mr-1" /> Back to Community
      </button>
      
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <div className="flex items-start gap-4">
            <Avatar className="h-10 w-10">
              {isExploreUser ? (
                <img 
                  src={(user as ExtendedExploreUserData).avatarLink} 
                  alt={`${(user as ExtendedExploreUserData).firstName} ${(user as ExtendedExploreUserData).lastName}`} 
                />
              ) : (
                <img 
                  src={(user as ExtendedUserData).profilePicUrl} 
                  alt={(user as ExtendedUserData).name} 
                />
              )}
            </Avatar>
            <div className="flex flex-col justify-center">
              <CardTitle className="text-xl leading-tight">
                {isExploreUser 
                  ? `${(user as ExtendedExploreUserData).firstName} ${(user as ExtendedExploreUserData).lastName}`
                  : (user as ExtendedUserData).name
                }
              </CardTitle>
              <CardDescription className="text-base leading-tight">
                {isExploreUser 
                  ? (user as ExtendedExploreUserData).keyword1
                  : (user as ExtendedUserData).text1
                }
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Summary</h3>
              <p>{user.summary}</p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Portfolio Allocation</h3>
              <PortfolioAllocationChart
                category={user.category}
                totalPerformance={user.total_performance}
              />
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Risk Profile</h3>
              <RiskProfile riskRatio={user.sharpRatio} riskText={user.riskText} />
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Specialty</h3>
              <p>
                {isExploreUser 
                  ? (user as ExtendedExploreUserData).keyword2
                  : (user as ExtendedUserData).text2
                }
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 