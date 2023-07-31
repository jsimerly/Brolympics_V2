import {useState} from 'react'
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import ManageBro from '../manage/ManageBro';
import ManageEvents from '../manage/ManageEvents';
import ManageTeams from '../manage/ManageTeams';
import {fetchStartBrolympics} from '../../../api/activeBro/fetchAdmin'


const HomeAdminPre = ({teams, events, uuid, setStatus}) => {
  const onStartClick = async () => {
    const response = await fetchStartBrolympics(uuid)
    if (response.ok){
      setStatus('active')
    }
  }  
  
  return (
    <div className='min-h-[calc(100vh-220px)] bg-offWhite text-neutralDark p-6 flex flex-col gap-3'>
      <div className='w-full p-3 border rounded-md border-primary'>
        <h3 className='w-full font-semibold text-center'>Ready to Go?</h3>
        <div className='flex items-center justify-center w-full mt-3'>
          <button 
            className='w-1/2 p-2 font-bold text-white rounded-md bg-primary'
            onClick={onStartClick}
          >
            Start Brolympics
          </button>
        </div>
        
      </div>
      <h3 className='flex items-center w-full gap-3 text-errorRed'>
          <PriorityHighIcon/> 
          <span className='text-[12px]'>Make sure you fully update all of your event settings before your Brolympics begins.</span>
      </h3>
      <ManageEvents events={events}/>
      <div className='my-3'/>
      <ManageTeams teams={teams} broUUID={uuid}/>
      <div className='my-3'/>
      <ManageBro/>
    </div>
  )
}

export default HomeAdminPre