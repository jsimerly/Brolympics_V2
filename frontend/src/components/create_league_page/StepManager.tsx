
import CreateLeaguePage from "./CreateLeaguePage"
import CreateBrolympics from "./CreateBrolympics"
import AddEvent from "./AddEvent"
import AddPlayers from "./AddPlayers"

const StepManager = ({step, nextStep, prevStep}) => {

  return (
    <div
        className={`transition ease-in-out duration-200 flex
            w-full
        `}
        style={{transform: `translateX(-${100 * (step-1)}%`}}
    >
        <CreateLeaguePage step={1} nextStep={nextStep}/>
        <CreateBrolympics step={2} nextStep={nextStep}/>
        <AddEvent step={3} nextStep={nextStep}/>
        <AddPlayers step={4} nextStep={nextStep} prevStep={prevStep}/>
    </div>
  )
}

export default StepManager