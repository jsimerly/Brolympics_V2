import ManageEventWrapper from "./ManageEventWrapper"
import ToggleButton from "../../../Util/ToggleButton"
import {useState} from 'react'

const ScoringSettings = ({highScoreWins, highScoreToggle}) => {

  return (
    <>
        <h2 className="py-2">Scoring Settings</h2>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">Scoring Type (Decimal Places)</h3>
                    <p className="text-[10px]"> Is this event scored by whole numbers, decimal places, or just win/loss? Max decimal places: 16</p>
                </div>
                <input 
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                    type='number'
                />
            </div>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">High Score to Win</h3>
                    <p className="text-[10px]">Is this event won by the higher score or the lower score. <br/> Currently set to: <span className="font-bold">{highScoreWins ? 'High Score Wins' : 'Low Score Wins'}</span></p>
                </div>
                <button
                    onClick={highScoreToggle}
                    className="text-primary w-[60px]"
                >
                    <ToggleButton size={50} on={highScoreWins}/>
                </button>
            </div>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">Max Score</h3>
                    <p className="text-[10px]">Highest possible score. Leave blank for no max.</p>
                </div>
                <input 
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                    type='number'
                />
            </div>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">Min Score</h3>
                    <p className="text-[10px]">Lowest possible score. Leave blank for no min.</p>
                </div>
                <input 
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                    type='number'
                />
            </div>
            <h2 className="py-2">Date & Time</h2>
            <div className="flex flex-col w-full gap-3">
                <div className='flex flex-col'>
                    <span className='ml-1 text-[12px] font-semibold'>Start Date (optional)</span>
                    <input 
                    className='flex w-full p-2 border rounded-md border-primary'
                    type='datetime-local'
                    />
                </div>
                <div className='flex flex-col font-semibold'>
                    <span className='ml-1 text-[12px]'>End Date (options)</span>
                    <input 
                    className='flex w-full p-2 border rounded-md border-primary'
                    type='datetime-local'
                    />
                </div>
            </div>
    </>
  )
}

export default ScoringSettings