import{useState} from 'react'
import { Routes, Route, useNavigate, } from "react-router-dom"
import ExpandMoreOutlinedIcon from '@mui/icons-material/ExpandMoreOutlined';
import {useDropdown} from '../../../hooks'

const EventDropdown = ({events}) => {
    const [selectedEvent, setSelectedEvent] = useState(events[0])
    const navigate = useNavigate()
  
    const handleSelect = (event) => {
      setSelectedEvent(event)
      setIsOpen(false)
      navigate(`/brolympics/event/${event}`);
    }
  
    const [isOpen, setIsOpen, handleDropdownClicked, dropdownNode] = useDropdown()

  return (
    <div className='relative flex flex-col items-center justify-center w-full py-3 '>
        <div>
          <div 
            className=' flex justify-between items-center w-[200px] text-[20px] font-bold  border-neutralLight'
            onClick={handleDropdownClicked}
          >
            <h2 className='flex items-center justify-center w-full text-center'>
              {selectedEvent ? selectedEvent : 'Select a Event'}
            </h2> 
              <ExpandMoreOutlinedIcon/>
          </div>
          {isOpen && (
            <ul 
              className='absolute top-[50px] border p-2 rounded-md shadow-lg w-[200px] z-10 bg-neutral'
              ref={dropdownNode}
            >
              {events
                .filter((event) => event !== selectedEvent)
                .map((event, index) => (
                  <div key={index+"_dropdown"}>                
                    <li 
                      key={index+'_event'} 
                      className='text-[16px] py-2'
                      onClick={() => handleSelect(event)}
                    >
                      {event}
                    </li>
                    {index+2 !== events.length && 
                    <div key={index+'_divider'} className='w-full bg-gray-200 h-[1px]'/>}
                  </div>
                ))}
            </ul>
          )}
        </div>
      </div>
  )
}

export default EventDropdown