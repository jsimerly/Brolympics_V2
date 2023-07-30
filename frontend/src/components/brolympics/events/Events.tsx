import EventDropdown from './EventDropdown'
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
import DiamondOutlinedIcon from '@mui/icons-material/DiamondOutlined';
import MenuBookOutlinedIcon from '@mui/icons-material/MenuBookOutlined';
import Bracket from './Bracket';
import Comp_h2h from './Competitions/Comp_h2h';

import { fetchEventInfo } from '../../../api/activeBro/fetchEvents.js'
import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Events = ({events, default_uuid, default_type}) => {

  let {eventUuid, eventType} = useParams()
  let navigate = useNavigate
  const [eventInfo, setEventInfo] = useState()
  
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
        console.log(data)
        setEventInfo(data)
      }
    }
    getEventInfo()
  },[])

  const competitions = [
    {
      'winner' : 'Third Dynasty of Ur',
      'team_1_name' : 'Third Dynasty of Ur',
      'team_1_score' : 21,
      'team_2_name' : 'Poland',
      'team_2_score' : 8,
      'is_active': false,
      'is_complete' : true,
    },
    {
      'winner' : 'France',
      'team_1_name' : 'Third Dynasty of Ur',
      'team_1_score' : 21,
      'team_2_name' : 'France',
      'team_2_score' : 3,
      'is_active' : false,
      'is_complete' : true,
    },
    {
      'winner' : 'Third Dynasty of Ur',
      'team_1_name' : 'Greece',
      'team_1_score' : 5,
      'team_2_name' : 'Third Dynasty of Ur',
      'team_2_score' : 21,
      'is_active' : false,
      'is_complete' : true,
    },
    {
      'winner' : 'Third Dynasty of Ur',
      'team_1_name' : 'Third Dynasty of Ur',
      'team_1_score' : 21,
      'team_2_name' : 'Germany',
      'team_2_score' : 6,
      'is_active' : false,
      'is_complete' : true,
    },
    {
      'winner' : null,
      'team_1_name' : 'Third Dynasty of Ur',
      'team_1_score' : 0,
      'team_2_name' : 'Germany',
      'team_2_score' : 0,
      'is_active' : true,
      'is_complete' : false,
    },
  ]
  

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
                <td className='p-2 font-bold text-center text-[18px] border-r border-neutralLight'>{ranking.rank}</td>
                <td className='pl-6 text-start text-[20px] border-r border-neutralLight'>
                  {ranking.team.name}
                </td>
                <td className='p-2 text-center border-r text-[18px] border-neutralLight'>{ranking.points}</td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className='py-3'>
        {eventInfo &&
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
                <Comp_h2h {...comp} key={i}/>
                {i !== competitions.length - 1  && 
                  <div className="w-full px-6">
                    <div className="w-full h-[1px] bg-neutralLight" />
                  </div>
                  }
              </div>
            ))}
          </div>
        </div>
      }
      
    </div>
  )
}

export default Events