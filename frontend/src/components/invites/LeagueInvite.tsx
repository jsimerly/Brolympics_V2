import { useParams } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const LeagueInvite = () => {
    const {currentUser} = useContext(AuthContext)
    
  return (
    <div className="flex flex-col items-center justify-start w-full h-[calc(100vh-80px)]">
        LeagueInvite
    </div>
  )
}

export default LeagueInvite