import {useState} from 'react'
import {useHistory} from 'react'
import CreateEvent from './CreateEvent';

const CreateEventManger = ({addedEvents, setAddedEvents ,setH2hEvents, setIndEvents, setTeamEvents}) => {


    const handleEventAdded = (eventName, selectedType) => {
        setAddedEvents(prevEvents => [...prevEvents, eventName]);
        setEventName("");   

        let newEvent = {'name': eventName};
        if (selectedType === 'ind'){
          setIndEvents(prevEvents => [...prevEvents, newEvent])
        }
        if (selectedType === 'h2h'){
          setH2hEvents(prevEvents => [...prevEvents, newEvent])
        }
        if (selectedType == 'team'){
          setTeamEvents(prevEvents => [...prevEvents, newEvent])
        }
        console.log(addedEvents)
    }


  return (
    <div className="w-full">
        <CreateEvent handleEventAdded={handleEventAdded}/>
    </div>
  )
}

export default CreateEventManger