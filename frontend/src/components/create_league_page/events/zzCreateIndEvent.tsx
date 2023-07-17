import {useState, useEffect} from 'react'
import ArrowBackOutlinedIcon from '@mui/icons-material/ArrowBackOutlined';

const CreateIndEvent = ({setType, selected, handleEventSelected}) => {
  const [eventName, setEventName] = useState()
  const [scoreType, setScoreType] = useState()
  const [displayAvgScore, setDisplayAvgScore] = useState()
  const [nCompetitions, setNCompetitions] = useState(1)
  const [nActiveLimit, setNActiveLimit] = useState()


  const handleBackClick = () =>{
    setType(null)
  }
  const handleCreateEventClicked = () => {
    console.log("EVENT CREATED")
    setType(null)
  }
  useEffect(() => {
    if (selected === null){
      handleEventSelected()
    }
  }, [selected])
  
  return (
    <div>
      <div className='flex items-center justify-center w-full py-3 border-t border-neutral'>
        <button className='flex items-center w-1/3 gap-1 text-start' onClick={handleBackClick}>
          <ArrowBackOutlinedIcon/> Back
        </button>
        <h2 className='w-1/3 text-center text-[20px] font-bold'>Event Info</h2>
        <div className='w-1/3'/>
      </div>
      <div className='flex flex-col gap-3'>
        <div>
          <h3>Event Name *</h3>
          <input 
              type='text' 
              value={eventName} 
              onChange={(e) => setEventName(e.target.value)}
              placeholder='Enter the name of your league'
              className='w-full p-2 border border-gray-200 rounded-md'
            />
        </div>
        <div>
          <h3>Number of Competitions</h3>
          <p className='text-[10px]'>Number of times each team completes this event. Ex: Playing 2 rounds of golf.</p>
          <input 
              type='number' 
              value={nCompetitions} 
              onChange={(e) => setNCompetitions(e.target.value)}
              placeholder='# Competitions'
              className='w-[80px] p-2 border border-gray-200 rounded-md text-center'
            />
        </div>
      </div>
      <button>
        Advanced
      </button>
     

    </div>
  )
}

export default CreateIndEvent

// name
// score type
// max_score
// 
// display avg score
// n_competitions
// n_active_limit