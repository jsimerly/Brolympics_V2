import { useState, useEffect } from 'react'
import CreateWrapper from './CreateWrapper'
import CreateEventManger from './events/CreateEventManger'
import RemoveIcon from '@mui/icons-material/Remove';

const EventComp = ({header, events, setter}) => {
  const removeEvent = (i, events, setter) => {
    const newEvents = [...events];
    newEvents.splice(i, 1);
    setter(newEvents);
  }

  return(
    <>
      <h4>{header}</h4>
      <ul>
        {events.map((event, i) => (
          <li key={i} className='flex'>
            <button onClick={() => removeEvent(i, events, setter)}>
              <RemoveIcon className='mr-1 text-errorRed'/>
            </button>
            <p>{event.name}</p>
          </li>
        ))}
      </ul>
    </>
  )
}


const AddEvent = ({step, h2hEvents, indEvents, teamEvents, setH2hEvents, setIndEvents, setTeamEvents, createAll, setLink}) => {
    const handleCreateClicked = () => {
        createAll()
    }
    
    const total_events = h2hEvents.length + indEvents.length + teamEvents.length
    const is_event_added = total_events === 0
    const button_text = is_event_added ? 'Skip' : `Create ${total_events} Events`;

  return (
    <CreateWrapper
        button_text={button_text}
        grey_out={is_event_added}

        step={step}
        submit={handleCreateClicked}
        title={'Add Events to Your Brolympics'}
        description={'Add Events to your Brolympics. These are the events that will make up the entire competition.'}
    >
        <CreateEventManger 
          setH2hEvents={setH2hEvents}
          setIndEvents={setIndEvents}
          setTeamEvents={setTeamEvents}
        />
        <div>
          <h3 className='pt-6 text-[18px] font-bold text-neutralDark'>Your Events</h3>
          {indEvents.length > 0 &&
            <EventComp
              header='Individual Events'
              events={indEvents}
              setter={setIndEvents}
            />
          }
         
        </div>
    </CreateWrapper>
  )
}


export default AddEvent