import ManageEventWrapper from "./ManageEventWrapper"
import {useState} from 'react'
import ScoringSettings from "./ScoringSettings"
import ToggleButton from "../../../Util/ToggleButton"

const ManageEvent_ind = ({name}) => {
    const [highScoreWins, setHighScoreWins] = useState(true)
    const highScoreToggle = () => {
        setHighScoreWins(bool => !bool)
    }
    const [displayAvg, setDisplayAvg] = useState(false)
    const displayAvgToggle = () => {
        setDisplayAvg(bool => !bool)
    }
  return (
    <ManageEventWrapper name={name}>
                <h2 className="py-2">Competition Settings</h2>
        <div className="flex items-center justify-between min-h-[50px]">
            <div>
                <h3 className="font-semibold">Number of Competitions</h3>
                <p className="text-[10px]">The number of times each team will complete this event. Ex: Completing 2 relay races.</p>
            </div>
            <input 
                className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                type='number'
            />
        </div>
        <div className="flex items-center justify-between min-h-[50px]">
            <div>
                <h3 className="font-semibold">Max Concurrent Competitions</h3>
                <p className="text-[10px]">The number of max possible simulatnious competitions. <br/> Ex: 2 relay race courses. Leave blank for no max.</p>
            </div>
            <input 
                className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                type='number'
            />
        </div>
        <div className="flex items-center justify-between min-h-[50px]">
            <div>
                <h3 className="font-semibold">Display Average Scores</h3>
                <p className="text-[10px]"> Do you want to display average scores or combined scores? <br/> Currently set to: <span className="font-bold">{displayAvg ? 'Average Score' : 'Combined Score'}</span></p>
            </div>
            <button
                onClick={displayAvgToggle}
                className="text-primary w-[60px]"
            >
                <ToggleButton size={50} on={displayAvg}/>
            </button>
        </div>
        <ScoringSettings
            highScoreWins={highScoreWins} 
            highScoreToggle={highScoreToggle}
        />
        <button className="w-full p-2 mt-3 font-semibold text-white rounded-md bg-primary">
            Update {name}
        </button>
        <button className="w-full p-2 mt-3 font-semibold text-white rounded-md bg-errorRed">
            Delete
        </button>
    </ManageEventWrapper>
  )
}

export default ManageEvent_ind