import React from 'react'

const AvailableCompetition_ind = ({name, team_name, team_img}) => {
  return (
    <div className='p-2'>
        <h2 className='pb-2 font-bold'>{name}</h2>
        <div className='flex gap-2'>
            <div className='h-[60px] w-[60px] min-w-[60px] bg-white rounded-md'>
                img
            </div>
            <div className='flex items-center font-bold'>
                {team_name}
            </div>

        </div>
        <div className="flex items-center justify-center w-full pt-6">
            <button className='w-1/2 p-2 font-bold rounded-md bg-primary'>
            Start
            </button>
        </div>
    </div>
  )
}

export default AvailableCompetition_ind