import { useState } from "react"
import CreateLeaguePage from "./CreateLeaguePage"
import CreateBrolympics from "./CreateBrolympics"
import AddEvent from "./AddEvent"
import AddPlayers from "./AddPlayers"

const StepManager = ({step, nextStep, prevStep,}) => {
    const [league, setLeague] = useState({})
    const [brolympics, setBrolympics] = useState({})
    const [h2hEvents, setH2hEvents] = useState([])
    const [indEvents, setIndEvents] = useState([])
    const [teamEvents, setTeamEvents] = useState([])
    const [link, setLink] = useState()
    
    const createAll = () => {
        console.log('creating league, brolypics, and events')
    }
  return (
    <div
        className={`transition ease-in-out duration-200 flex
            w-full
        `}
        style={{transform: `translateX(-${100 * (step-1)}%`}}
    >
        <CreateLeaguePage 
          step={1} 
          nextStep={nextStep} 
          setLeague={setLeague}
        />
        <CreateBrolympics 
          step={2} 
          nextStep={nextStep} 
          setBrolympics={setBrolympics}
        />
        <AddEvent 
          step={3} 
          nextStep={nextStep} 
          setH2hEvents={setH2hEvents} 
          setIndEvents={setIndEvents} 
          setTeamEvents={setTeamEvents} 
          createAll={createAll} 
          setLink={setLink}
        />
        <AddPlayers 
          step={4} 
          nextStep={nextStep} 
          prevStep={prevStep} 
          link={link}
        />
    </div>
  )
}

export default StepManager