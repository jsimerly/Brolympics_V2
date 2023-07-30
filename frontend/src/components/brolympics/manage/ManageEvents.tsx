import React, {useState} from 'react'
import { useParams } from 'react-router-dom';
import {fetchCreateEvent} from '../../../api/fetchEvents.js'

import ManageEvent_h2h from './events/ManageEvent_h2h'
import ManageEvent_ind from './events/ManageEvent_ind'
import ManageEvent_team from './events/ManageEvent_team'

import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import CreateEvent from '../../create_league_page/events/CreateEvent';
import RemoveIcon from '@mui/icons-material/Remove';


const ManageEvents = ({events}) => {
    const [addingEvent, setAddingEvent] = useState(false)
    const [compEvents, setCompEvents] = useState(events)
    const {uuid} = useParams()

    console.log(events)
    const toggleAddEvent = () => {
        setAddingEvent(addingEvent => !addingEvent)
    }

    const handleEventAdd = async (eventName, type) => {
        const response = await fetchCreateEvent(eventName, type, uuid)
        if (response.ok){
            setCompEvents(prevEvents => [
                ...prevEvents,
                {'name': eventName, 'type':type}
            ])
            setAddingEvent(false)
        }
    }

    const CompToType = {
        'h2h' : <ManageEvent_h2h/>,
        'ind' : <ManageEvent_ind/>,
        'team' : <ManageEvent_team/>
    }

  return (
    <div className=''>
        <h2 className='font-bold text-[16px]'>Manage Events </h2>
        <div>
            {compEvents &&
                compEvents.map((event, i) => (
                    <>
                        {i !== 0 && <div className='w-full h-[1px] bg-neutralLight'/>}
                        {React.cloneElement(CompToType[event.type], {key: i+"_eventCard", event: event})}
                        
                    </>
                ))
            }
        </div>
        <button
            className='flex gap-3  text-[16px] text-neutralLight'
            onClick={toggleAddEvent}
        >
            Add Event
            {addingEvent ? <RemoveIcon/> : <AddCircleOutlineIcon/> }
        </button>
        {addingEvent &&
            <CreateEvent
                handleEventAdded={handleEventAdd}
            />
        }
    </div>
  )
}

export default ManageEvents