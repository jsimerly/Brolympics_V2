import { useState } from "react"
import CreateLeaguePage from "./CreateLeaguePage.jsx"
import CreateBrolympics from "./CreateBrolympics.jsx"
import AddEvent from "./AddEvent.jsx"
import AddPlayers from "./AddPlayers.jsx"
import { createAllLeague} from '../../api/fetchLeague.js'

const StepManager = ({step, nextStep, prevStep,}) => {
    const [league, setLeague] = useState({})
    const [brolympics, setBrolympics] = useState({})
    const [h2hEvents, setH2hEvents] = useState([])
    const [indEvents, setIndEvents] = useState([])
    const [teamEvents, setTeamEvents] = useState([])
    const [link, setLink] = useState()
    
    const createAll = async () => {
      const response = await createAllLeague(
        league,
        brolympics,
        h2hEvents,
        indEvents,
        teamEvents
      )
      if (response.ok){
        const data = await response.json()
        setLink(data.uuid)
        console.log(data)
        nextStep()
      } else {
        const data = await response.json()
        console.log(data)
      }
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