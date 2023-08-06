import EventDropdown from './EventDropdown'
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
import DiamondOutlinedIcon from '@mui/icons-material/DiamondOutlined';
import MenuBookOutlinedIcon from '@mui/icons-material/MenuBookOutlined';
import Bracket from './Bracket';
import Comp_h2h from './Competitions/Comp_h2h';

import { fetchEventInfo } from '../../../api/activeBro/fetchEvents.js'
import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Comp_ind from './Competitions/Comp_ind.jsx';
import Comp_team from './Competitions/Comp_team.jsx';

const Events = ({events, default_uuid, default_type}) => {

  let {eventUuid, eventType} = useParams()
  let navigate = useNavigate
  const [eventInfo, setEventInfo] = useState()

  const getFontSize = (name) => {
    if (name){
      if (name.length <= 12){
        return '18px'
      } else if (name.length <= 16){
        return '16px'
      } else if (name.length <= 20){
        return '14px'
      } else {
        return '14px'
      }
    }
  }

  const getDisplayInfo = (ranking) => {
    if (eventInfo.type === 'h2h'){
      return `${ranking.wins}-${ranking.losses} 
      ${ranking.ties != 0 ? `${ranking.ties}` : ''}`
    }
  }
  
  useEffect(()=>{
    if (!eventUuid && default_uuid && default_type){
      navigate(`/team/${default_type}/${default_uuid}`)
    }
  },[eventUuid])

  useEffect(()=>{
    const getEventInfo =  async () => {
      const response = await fetchEventInfo(eventUuid,eventType)
      if (response.ok) {
        const data = await response.json()
        setEventInfo(data)
      }
    }
    getEventInfo()
  },[eventUuid])

  const componentMap = {
    'h2h' : Comp_h2h,
    'ind' : Comp_ind,
    'team' : Comp_team,
  }

  const CompComp = componentMap[eventInfo?.type] || Comp_ind  

  return (
    <div className=''>
      <EventDropdown events={events}/>
      <div className=''>
        <div className='flex items-center justify-between px-6 pb-2'>
          <h2 className='font-bold text-[20px]'>Standings</h2>
          <div className='flex flex-col items-start justify-center'>
            <MenuBookOutlinedIcon sx={{fontSize:30}}/> 
          </div>
        </div>
        <div className='px-6'>
          <table className='w-full border border-neutralLight'>
            <thead>
              <tr className='border text-primary border-neutralLight'>
                <th className='border border-neutralLight w-[60px] p-2'><NumbersOutlinedIcon/></th>
                <th className='pl-6 border border-neutralLight text-start text-[20px]'>Team</th>
                <th className='border border-neutralLight w-[80px]'><DiamondOutlinedIcon/>
                </th>
              </tr>
            </thead>
            <tbody>
            {
              eventInfo &&
              eventInfo.standings
                .sort((a, b) => a.rank - b.rank) 
                .map((ranking, i) => (
              <tr key={i+'_row'}>
                <td className='p-3 font-semibold text-center text-[18px] border-r border-neutralLight'>{ranking.rank}</td>
                <td className='pl-3 text-start text-[20px] border-r border-neutralLight'>
                  <div className='flex items-center gap-2'>
                    <img src={ranking.team.img} className='w-[30px] h-[30px] rounded-md'/>
                    <div className='flex flex-col justify-center'>
                      <span className={`text-[${getFontSize(ranking.team.name)}] leading-5`}>
                        {ranking.team.name}
                      </span>
                      <span className='text-[10px]'>{getDisplayInfo(ranking)}</span>
                    </div>
                  </div>
                </td>
                <td className='p-2 text-center border-r text-[18px] border-neutralLight'>
                {Number.isInteger(ranking?.points) ? ranking.points : ranking.points.toFixed(1)}</td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className='py-3'>
        {eventInfo && eventInfo?.type === 'h2h' &&
          <Bracket
            {...eventInfo.bracket}     
          />
        }

      </div>
      {eventInfo &&
        <div className='pb-6'>
          <h2 className='font-bold text-[20px] px-6'>Competitions</h2>
          <div>
            {eventInfo.competitions.map((comp, i) => (
              <div key={i+"_events"}>
                  {i !== 0  && 
                  <div className="w-full px-6">
                    <div className="w-full h-[1px] bg-neutralLight" />
                  </div>
                  }
                <CompComp {...comp} key={i}/>
              </div>
            ))}
          </div>
        </div>
      }
      
    </div>
  )
}

export default Events