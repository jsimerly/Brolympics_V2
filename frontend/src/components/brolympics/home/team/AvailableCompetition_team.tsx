import React from 'react'

const AvailableCompetition_team = ({name, team_name}) => {
    return (
        <div className='p-2 border border-gray-200 rounded-md'>
            <h2 className='pb-2 font-bold'>{name}</h2>
            <div className='flex gap-2'>
                <div className='h-[60px] w-[60px] min-w-[60px] bg-white rounded-md'>
                    img
                </div>
                <div className='flex items-center font-bold'>
                    {team_name}
                </div>
            </div>
        </div>
      )
    }

export default AvailableCompetition_team