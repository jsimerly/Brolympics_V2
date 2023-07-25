import React, {useState} from 'react'
import ManageEvent_h2h from './events/ManageEvent_h2h'
import ManageEvent_ind from './events/ManageEvent_ind'
import ManageEvent_team from './events/ManageEvent_team'

import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import CreateEvent from '../../create_league_page/events/CreateEvent';
import RemoveIcon from '@mui/icons-material/Remove';


const ManageEvents = () => {
    const [addingEvent, setAddingEvent] = useState(false)
    const toggleAddEvent = () => {
        setAddingEvent(addingEvent => !addingEvent)
    }

    const handleEventAdd = () => {
        console.log('Add event here')
        setAddingEvent(false)
    }

    const events = [
        {'name' : 'Cornholio', 'type':'h2h'},
        {'name' : 'Golf', 'type':'ind'},
        {'name' : 'Trivia', 'type':'team'}
    ]

    const CompToType = {
        'h2h' : <ManageEvent_h2h/>,
        'ind' : <ManageEvent_ind/>,
        'team' : <ManageEvent_team/>
    }

  return (
    <div className=''>
        <h2 className='font-semibold text-[20px]'>Manage Events </h2>
        <div>
            {events &&
                events.map((event, i) => (
                    <>
                        {i !== 0 && <div className='w-full h-[1px] bg-neutralLight'/>}
                        {React.cloneElement(CompToType[event.type], {key: i, ...event})}
                        
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