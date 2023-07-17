import {useState} from 'react'
import {useHistory} from 'react'
import CreateEvent from './CreateEvent';

const CreateEventManger = ({addedEvents, setAddedEvents}) => {
    const [selectedType, setSelectedType] = useState('ind');
    const [eventName, setEventName] = useState("")

    const handleEventAdded = () => {
        setAddedEvents(prevEvents => [...prevEvents, eventName]);
        setEventName("");   
        console.log(addedEvents)
    }


  return (
    <div className="w-full">
        <CreateEvent 
            selected={selectedType} 
            setType={setSelectedType} 
            handleEventAdded={handleEventAdded}
            eventName={eventName}
            setEventName={setEventName}
        />
    </div>
  )
}

export default CreateEventManger