import { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation, useParams} from "react-router-dom"
import Toolbar from "./toolbar/Toolbar"
import Events from "./events/Events"
import Standings from "./standings/Standings"
import Home from "./home/Home"
import Team from "./team/Team"
import InCompetition from './InCompetition';
import ManageRouter from './manage/ManageRouter.js';
import {fetchBrolympicsHome, fetchInCompetition} from '../../api/fetchBrolympics.js'

const Brolympics = () => {

  const [broInfo, setBroInfo] = useState()
  const {uuid} = useParams()

  const [status, setStatus] = useState('active')

  useEffect(() => {
    if (broInfo) {
      broInfo.is_active && setStatus('active');
      !broInfo.is_active && !broInfo.is_complete && broInfo.is_owner && setStatus('pre_admin');
      !broInfo.is_active && !broInfo.is_complete && !broInfo.is_owner && setStatus('pre');
      broInfo.is_complete && setStatus('post');
    }
  }, [broInfo]); 

  useEffect(()=> {
    const getBrolympicsInfo = async () => {
      const response = await fetchBrolympicsHome(uuid)
      
      if (response.ok){
        const data = await response.json()
        setBroInfo(data)
        console.log(data)
      } else {
        
      }
    } 
    getBrolympicsInfo()
  },[])

  const navigate = useNavigate();
  const location = useLocation();
  const page = location.pathname.split("/")[3]

  const [activeComp, setActiveComp] = useState({
    is_available: true,
    comp_uuid: '',
    type: ''
  })

  useEffect(() => {
    if (broInfo && broInfo.is_active){
      const getIsAvailable = async () => {
        const response = await fetchInCompetition()

        if (response.ok){
          const data = await response.json()
          if (!data.is_available){
            if (activeComp.is_available){
              setActiveComp(data)
              console.log(data)
            }

            if (!location.pathname.includes(
              `/b/${uuid}/competition/${data.comp_uuid}`
            )){
              navigate(`/b/${uuid}/competition/${data.comp_uuid}`)
            }
          }

          if (data.is_available){
            if (!activeComp.is_available){
              setActiveComp(data)
            }

            if (location.pathname.includes(
              `/b/${uuid}/competition/`
            )){
              navigate(`/b/${uuid}/home`)
            }
          }
        }
      }
      getIsAvailable()

    }
  }, [location, broInfo]);

  return (
    <div className='bg-neutral min-h-[calc(100vh-80px)] text-white'>
      <div 
        className={`w-full p-3 text-center 
         ${page === 'manage' || (status === 'pre_admin' && page === 'home') ?  'bg-offWhite text-neutralDark': 'border-b border-neutralLight'} `
        }
      >
        <h1 className='w-full font-bold leading-none text-[30px] '>
          Summer 2023
        </h1>
        <span>Stuck in Highschool</span>
      </div>
        <Routes>
            <Route path="home" element={<Home brolympics={broInfo} status={status} setStatus={setStatus}/>} />
            <Route path="standings" element={<Standings />} />
            
            <Route path="team/:teamUuid" element={
              <Team 
                teams={broInfo?.teams} 
                default_uuid={broInfo?.team_uuid}
              />} 
            />
            <Route path="event/:eventType/:eventUuid" element={
              <Events 
                events={broInfo?.events} 
                default_uuid={broInfo?.events[0].uuid}
                default_type={broInfo?.events[0].type}
              />} 
            />
            <Route path='competition/:compUuid' element={<InCompetition activeComp={activeComp}/>}/>
            <Route path='manage/*' element={<ManageRouter brolympics={broInfo}/>}/>
        </Routes>
        {activeComp.is_available && 
          <Toolbar
            is_owner={broInfo?.is_owner}
            default_team_uuid = {broInfo?.team_uuid || ''}
            default_event_type = {broInfo?.events[0].type}
            default_event_uuid = {broInfo?.events[0].uuid}
          />
        }
    </div>
  )
}

export default Brolympics