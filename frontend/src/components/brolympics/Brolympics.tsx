import { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation, useParams} from "react-router-dom"
import Toolbar from "./toolbar/Toolbar"
import Events from "./events/Events"
import Standings from "./standings/Standings"
import Home from "./home/Home"
import Team from "./team/Team"
import InCompetition from './InCompetition';
import ManageRouter from './manage/ManageRouter.js';
import {fetchBrolympicsHome} from '../../api/fetchBrolympics.js'

const Brolympics = () => {
  const [activeComp, setActiveComp] = useState(null)
  const [broInfo, setBroInfo] = useState()
  const [is_available, setIsAvailable]= useState(activeComp === null)
  const {uuid} = useParams()
  
  
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(()=> {
    const getBrolympicsInfo = async () => {
      const response = await fetchBrolympicsHome(uuid)
      
      if (response.ok){
        const data = await response.json()
        setBroInfo(data)
      } else {
        
      }
    } 
    getBrolympicsInfo()
  },[])

  const page = location.pathname.split("/")[3]

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
      <div 
        className={`w-full p-3 text-center 
         ${page !== 'manage' ? 'border-b border-neutralLight' : 'bg-offWhite text-neutralDark'} `
        }
      >
        <h1 className='w-full font-bold leading-none text-[30px] '>
          Summer 2023
        </h1>
        <span>Stuck in Highschool</span>
      </div>
        <Routes>
            <Route index element={<Home/>}/>
            <Route path="home" element={<Home />} />
            <Route path="standings" element={<Standings />} />
            <Route path="team" element={<Team />} />
            <Route path="team/:teamUuid" element={<Team />} />
            <Route path="event" element={<Events />} />
            <Route path="event/:eventUuid" element={<Events />} />
            <Route path='competition/:compUuid' element={<InCompetition comp={activeComp}/>}/>
            <Route path='manage/*' element={<ManageRouter/>}/>
            <Route 
                path="*" 
                element={<Navigate to="home" replace/>} 
            />
        </Routes>
        {is_available &&
          <Toolbar
            is_owner={broInfo?.is_owner}
          />
        }
        
    </div>
  )
}

export default Brolympics