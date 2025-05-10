import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card"
import { useState } from "react"
import { ChevronDown, ChevronUp, Volume2, VolumeX } from "lucide-react"
import { UserCarousel, UserData } from "@/components/UserCarousel"
import { UserExplorer, ExploreUserData } from "@/components/UserExplorer"
import { useNavigate } from "react-router-dom"

export function CommunityPage() {
  // State to track if the card is expanded
  const [isExpanded, setIsExpanded] = useState(false);
  // State to track if text is being read aloud
  const [isReading, setIsReading] = useState(false);
  // Get navigation function
  const navigate = useNavigate();
  
  // Dummy AI summary text
  const summaryPreview = "This is an overall AI summary...";
  const fullSummary = "This is an overall AI summary of the community activity. The text will dynamically update based on user interactions, posts, and other community engagements. It provides insights about trending topics, active discussions, and overall community health.";

  // Sample data for the user explorer component
  const exploreUsers: ExploreUserData[] = [
    {
      id: "101",
      avatarLink: "https://i.pravatar.cc/300?img=11",
      firstName: "David",
      lastName: "Garcia",
      keyword1: "Crypto",
      keyword2: "Tech Stocks"
    },
    {
      id: "102",
      avatarLink: "https://i.pravatar.cc/300?img=12",
      firstName: "Sarah",
      lastName: "Miller",
      keyword1: "ESG",
      keyword2: "Green Energy"
    },
    {
      id: "103",
      avatarLink: "https://i.pravatar.cc/300?img=13",
      firstName: "Robert",
      lastName: "Kim",
      keyword1: "Real Estate",
      keyword2: "Bonds"
    },
    {
      id: "104",
      avatarLink: "https://i.pravatar.cc/300?img=14",
      firstName: "Jennifer",
      lastName: "Thompson",
      keyword1: "Startups",
      keyword2: "Angel Investing"
    },
    {
      id: "105",
      avatarLink: "https://i.pravatar.cc/300?img=15",
      firstName: "Ahmed",
      lastName: "Hassan",
      keyword1: "Commodities",
      keyword2: "Forex"
    },
    {
      id: "106",
      avatarLink: "https://i.pravatar.cc/300?img=16",
      firstName: "Lisa",
      lastName: "Wong",
      keyword1: "Dividends",
      keyword2: "Value Investing"
    }
  ];

  // Function to handle text-to-speech
  const handleTextToSpeech = () => {
    if (isReading) {
      window.speechSynthesis.cancel();
      setIsReading(false);
      return;
    }

    // Always read the full summary text
    const utterance = new SpeechSynthesisUtterance(fullSummary);
    
    utterance.onend = () => {
      setIsReading(false);
    };
    
    window.speechSynthesis.speak(utterance);
    setIsReading(true);
  };

  // Handle user selection from carousel
  const handleUserSelect = (user: UserData) => {
    navigate(`/community/user/${user.id}`);
  };

  // Handle user selection from explorer
  const handleExploreUserSelect = (user: ExploreUserData) => {
    navigate(`/community/user/${user.id}`);
  };

  return (
    <div className="container mx-auto space-y-8">
      {/* AI Summary Card */}
      <Card className="w-full max-w-4xl mx-auto mt-6">
        {!isExpanded ? (
          // Collapsed view
          <div className="flex justify-between items-center px-6">
            <div className="flex gap-2 items-center">
              <CardTitle className="text-base">Overall AI Summary:</CardTitle>
              <span className="text-sm text-muted-foreground">{summaryPreview}</span>
            </div>
            <div className="flex gap-2">
              <button 
                onClick={handleTextToSpeech}
                className="text-muted-foreground hover:text-primary"
                title={isReading ? "Stop reading" : "Read aloud full summary"}
              >
                {isReading ? <VolumeX size={16} /> : <Volume2 size={16} />}
              </button>
              <button 
                onClick={() => setIsExpanded(true)}
                className="text-muted-foreground hover:text-primary"
              >
                <ChevronDown size={16} />
              </button>
            </div>
          </div>
        ) : (
          // Expanded view
          <>
            <div className="flex justify-between items-center px-6 pt-4">
              <CardTitle>Overall AI Summary</CardTitle>
              <div className="flex gap-2">
                <button 
                  onClick={handleTextToSpeech}
                  className="text-muted-foreground hover:text-primary"
                  title={isReading ? "Stop reading" : "Read aloud full summary"}
                >
                  {isReading ? <VolumeX size={16} /> : <Volume2 size={16} />}
                </button>
                <button 
                  onClick={() => setIsExpanded(false)}
                  className="text-muted-foreground hover:text-primary"
                >
                  <ChevronUp size={16} />
                </button>
              </div>
            </div>
            <CardContent>
              <CardDescription className="mb-2">AI-generated insights about community activity</CardDescription>
              <p className="text-sm">{fullSummary}</p>
            </CardContent>
          </>
        )}
      </Card>
      
      {/* Community Members Section */}
      <div className="w-full">
        <h2 className="text-2xl font-bold text-center">Community Members</h2>
        <UserCarousel onUserSelect={handleUserSelect} />
      </div>

      {/* Explore Users Section */}
      <div className="w-full pb-8">
        <h2 className="text-2xl font-bold text-center mb-6">Explore More Users</h2>
        <UserExplorer users={exploreUsers} onUserSelect={handleExploreUserSelect} />
      </div>
    </div>
  )
} 