import { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom"
import Toolbar from "./toolbar/Toolbar"
import Events from "./events/Events"
import Standings from "./standings/Standings"
import Home from "./home/Home"
import Team from "./team/Team"
import InCompetition from './InCompetition';

const Brolympics = () => {
  
  const [activeComp, setActiveComp] = useState({
    'name' : 'Go Karting',
    'type' : 'team',
    'team_name' : 'Third Dynasty of Ur',
    'player_1_name' : 'Jacob Simerly',
    'player_2_name' : 'Frank Sergi',
    'decimal_places' : 3,
    'max_score' : 40,
    'min_score' : 20,
  }
  )
  const [is_available, setIsAvailable]= useState(activeComp === null)
  
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!is_available) {
      setIsAvailable(activeComp === null)
      navigate('/brolympics/competition');
    } else if (location.pathname === '/brolympics/competition') {
      navigate('/brolympics/home');
    }
  }, [activeComp, navigate]);

  return (
    <div className='bg-neutral min-h-[calc(100vh-80px)] text-white'>
      <div className='w-full p-3 text-center border-b border-neutralLight'>
        <h1 className='w-full font-bold leading-none text-[30px] '>
          Summer 2023
        </h1>
        <span>Stuck in Highschool</span>
      </div>
        <Routes>
            <Route path="/home" element={<Home />} />
            <Route path="/standings" element={<Standings />} />
            <Route path="/team" element={<Team />} />
            <Route path="/team/:teamName" element={<Team />} />
            <Route path="/event" element={<Events />} />
            <Route path="/event/:eventName" element={<Events />} />
            <Route path='/competition' element={<InCompetition comp={activeComp}/>}/>
            <Route 
                path="*" 
                element={<Navigate to="home" replace/>} 
            />
        </Routes>
        {is_available &&
          <Toolbar/>
        }
        
    </div>
  )
}

export default Brolympics