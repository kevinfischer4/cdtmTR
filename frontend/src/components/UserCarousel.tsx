import { useState, useRef, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface Friend {
  firstName: string;
  lastName: string;
  traderProfile: string;
  latest: string;
  avatarLink: string;
}

export interface UserData {
  id: string;
  profilePicUrl: string;
  name: string;
  text1: string;
  text2: string;
}

interface UserCarouselProps {
  className?: string;
  onUserSelect?: (user: UserData) => void;
  userId?: string;
}

export function UserCarousel({ className = "", onUserSelect, userId = "00909ba7-ad01-42f1-9074-2773c7d3cf2c" }: UserCarouselProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [transitioning, setTransitioning] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch friends data from API
  useEffect(() => {
    const fetchFriends = async () => {
      try {
        setLoading(true);
        const response = await fetch(`https://cdtmtr-backend-e2b85473091c.herokuapp.com/friends/?user_id=${userId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch friends data');
        }
        
        const friendsData: Friend[] = await response.json();
        
        // Map API data to UserData format
        const mappedUsers = friendsData.map((friend, index) => ({
          id: index.toString(), // Using index as id since API doesn't provide one
          profilePicUrl: friend.avatarLink || "https://via.placeholder.com/150",
          name: `${friend.firstName} ${friend.lastName}`,
          text1: friend.traderProfile || "No profile information available",
          text2: friend.latest || "No recent activity",
        }));
        
        setUsers(mappedUsers);
      } catch (err) {
        console.error("Error fetching friends:", err);
        setError("Failed to load friends data");
      } finally {
        setLoading(false);
      }
    };

    fetchFriends();
  }, [userId]);

  // Minimum swipe distance (in px)
  const minSwipeDistance = 50;

  // Check if screen is mobile size on mount and window resize
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    // Initial check
    checkMobile();
    
    // Add resize listener
    window.addEventListener('resize', checkMobile);
    
    // Cleanup
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handlePrev = () => {
    if (transitioning || users.length <= 1) return;
    setTransitioning(true);
    setActiveIndex((prevIndex) => (prevIndex === 0 ? users.length - 1 : prevIndex - 1));
  };

  const handleNext = () => {
    if (transitioning || users.length <= 1) return;
    setTransitioning(true);
    setActiveIndex((prevIndex) => (prevIndex === users.length - 1 ? 0 : prevIndex + 1));
  };

  const handleTransitionEnd = () => {
    setTransitioning(false);
  };

  const handleCardClick = (user: UserData) => {
    if (onUserSelect) {
      onUserSelect(user);
    }
  };

  // Touch event handlers
  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      handleNext();
    } else if (isRightSwipe) {
      handlePrev();
    }
  };

  // Calculate the position and styling for each card
  const getCardPosition = (index: number) => {
    if (users.length <= 1) return { 
      transform: "translateX(0)", 
      scale: "scale-100", 
      opacity: "opacity-100", 
      zIndex: "z-10",
      display: "" 
    };

    // Calculate relative position from active index
    const relativePosition = (((index - activeIndex) % users.length) + users.length) % users.length;
    
    // Default styles and positions
    let transform = "translateX(0)";
    let scale = "scale-75";
    let opacity = "opacity-60";
    let zIndex = "z-0";
    let display = "";
    
    // Consistent experience across all devices - always show 3 cards
    if (relativePosition === 0) {
      // Center (active) card
      transform = "translateX(0)";
      scale = "scale-100";
      opacity = "opacity-100";
      zIndex = "z-10";
    } else if (relativePosition === 1 || (users.length === 2 && relativePosition === 1)) {
      // Right card
      transform = isMobile ? "translateX(50%)" : "translateX(75%)";
      scale = "scale-75";
      opacity = "opacity-70";
      zIndex = "z-0";
    } else if (relativePosition === users.length - 1) {
      // Left card
      transform = isMobile ? "translateX(-50%)" : "translateX(-75%)";
      scale = "scale-75";
      opacity = "opacity-70";
      zIndex = "z-0";
    } else {
      // Hide other cards
      transform = relativePosition < users.length / 2 ? "translateX(-150%)" : "translateX(150%)";
      scale = "scale-50";
      opacity = "opacity-0";
      zIndex = "z-0";
      display = "none";
    }
    
    return { transform, scale, opacity, zIndex, display };
  };

  if (loading) {
    return <div className="flex justify-center items-center h-[380px]">Loading friends...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-[380px] text-red-500">{error}</div>;
  }

  if (users.length === 0) {
    return <div className="flex justify-center items-center h-[380px]">No friends found</div>;
  }

  return (
    <div className={`relative w-full max-w-4xl mx-auto overflow-hidden px-6 ${className}`}>
      {/* Carousel Controls */}
      {users.length > 1 && (
        <>
          <div className="absolute inset-y-0 left-0 flex items-center pl-1">
            <button 
              onClick={handlePrev}
              className="h-8 w-8 md:h-10 md:w-10 flex items-center justify-center rounded-full bg-background shadow-md z-20"
              disabled={transitioning}
              aria-label="Previous slide"
            >
              <ChevronLeft size={isMobile ? 16 : 20} />
            </button>
          </div>
          
          <div className="absolute inset-y-0 right-0 flex items-center pr-1">
            <button 
              onClick={handleNext}
              className="h-8 w-8 md:h-10 md:w-10 flex items-center justify-center rounded-full bg-background shadow-md z-20"
              disabled={transitioning}
              aria-label="Next slide"
            >
              <ChevronRight size={isMobile ? 16 : 20} />
            </button>
          </div>
        </>
      )}
      
      {/* Carousel Content */}
      <div
        ref={containerRef}
        className="relative flex justify-center items-center h-[380px] md:h-[450px] pointer-events-none"
        onTransitionEnd={handleTransitionEnd}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        {users.map((user, index) => {
          const { transform, scale, opacity, zIndex, display } = getCardPosition(index);
          return (
            <Card
              key={user.id}
              className={`absolute transition-all duration-500 ease-in-out w-[180px] md:w-[320px] ${scale} ${opacity} ${zIndex} pointer-events-auto cursor-pointer hover:shadow-lg`}
              style={{ transform, display }}
              onClick={() => handleCardClick(user)}
            >
              <CardContent className="p-4 md:p-8 flex flex-col items-center">
                <Avatar className="h-20 w-20 md:h-32 md:w-32 mb-4 md:mb-6">
                  <img src={user.profilePicUrl} alt={user.name} />
                </Avatar>
                <h3 className="text-base md:text-2xl font-semibold mb-2 md:mb-3 text-center">{user.name}</h3>
                <p className="text-xs md:text-sm text-muted-foreground text-center mb-2 md:mb-3 line-clamp-3">{user.text1}</p>
                <p className="text-xs md:text-sm text-muted-foreground text-center line-clamp-3">{user.text2}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>
      
      {/* Indicators */}
      {users.length > 1 && (
        <div className="flex justify-center md:mt-10 gap-1 md:gap-2">
          {users.map((_, index) => (
            <button
              key={index}
              className={`h-1.5 w-1.5 md:h-2 md:w-2 rounded-full ${
                index === activeIndex ? "bg-primary" : "bg-muted"
              }`}
              onClick={() => setActiveIndex(index)}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
} 