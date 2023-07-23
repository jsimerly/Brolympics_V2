import {useState} from 'react'
import {useHistory} from 'react'
import CreateEvent from './CreateEvent';

const CreateEventManger = ({addedEvents, setAddedEvents ,setH2hEvents, setIndEvents, setTeamEvents}) => {
    const [selectedType, setSelectedType] = useState('ind');
    const [eventName, setEventName] = useState("")

    const handleEventAdded = () => {
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