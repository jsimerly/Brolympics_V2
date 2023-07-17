import { useState, useEffect } from 'react'
import CreateWrapper from './CreateWrapper'
import CreateEventManger from './events/CreateEventManger'

const AddEvent = ({step, nextStep}) => {
    const [addedEvents, setAddedEvents] = useState([])
    let is_event_added = !(addedEvents.length === 0)

    const handleCreateClicked = () => {
        console.log('CREATE Event')
        nextStep()
    }

    useEffect(() => {
      is_event_added = !(addedEvents.length === 0)
    },[addedEvents])

    const button_text = !is_event_added ? 'Skip' : `Create ${addedEvents.length} Events`;

  return (
    <CreateWrapper
        button_text={button_text}
        grey_out={!is_event_added}

        step={step}
        submit={handleCreateClicked}
        title={'Add Events to Your Brolympics'}
        description={'Add Events to your Brolympics. These are the events that will make up the entire competition.'}
    >
        <CreateEventManger 
          addedEvents={addedEvents} 
          setAddedEvents={setAddedEvents}
        />
        <div>
          <h3 className='pt-6 text-[18px] font-bold text-neutralDark'>Your Events</h3>
          {is_event_added ? 
            <ul>
              {
                addedEvents.map((event, i) => (
                  <li key={i}>
                    {event}
                  </li>
                ))
              }
            </ul>
            :
            'You have not added any events.'
          }
        </div>
    </CreateWrapper>
  )
}


export default AddEvent