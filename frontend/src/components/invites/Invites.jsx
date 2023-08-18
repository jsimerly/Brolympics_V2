import { useContext, useEffect } from "react"
import { AuthContext } from "../../context/AuthContext"
import { Route, Routes,  useLocation } from "react-router-dom"
import LeagueInvite from "./LeagueInvite"
import BrolympicsInvite from "./BrolympicsInvite"
import TeamInvite from "./TeamInvite"
import SignUp from "../login_page/SignUp"

const Invites = () => {
    const {currentUser} = useContext(AuthContext)
    const location = useLocation()
    const returnPath = location.pathname
    location.reload()

  return (
    <div className="bg-offWhite text-neutralDark">
      {currentUser ? 
          <Routes>
            <Route path='league/:uuid' element={<LeagueInvite/>}/>
            <Route path='brolympics/:uuid' element={<BrolympicsInvite/>}/>
            <Route path='team/:uuid' element={<TeamInvite/>}/>
          </Routes>
        :
        <SignUp endPath={returnPath}/>
      }

    </div>
  )
}

export default Invites