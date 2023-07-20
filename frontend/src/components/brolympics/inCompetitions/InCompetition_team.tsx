import { useState } from 'react'

const InCompetition_team = ({team_name, name, decimal_places, max_score, min_score}) => {
    const [teamScore, setTeamScore] = useState(0)

    const getFontSize = (name) => {
        if (name) {
          if (name.length <= 10) {
              return '30px';
          } else if (name.length <= 16) {
              return '28px';
          } else if (name.length <= 20) {
              return '26px';
          } else {
              return '22px'
          }
        }
      }

      const isValidScore = (score) => {
        return score >= min_score && score <= max_score
      }
    
      const handleSumbitClicked = () => {
        if (isValidScore(teamScore)){
          console.log(1)
        }
      }

  return (
<div className='min-h-[calc(100vh-160px)] flex flex-col justify-between p-6'>
      <div>
      <h2 className=' w-full text-center text-[20px] mb-3'>
       {name}
      </h2>
      <div className='flex items-center w-full gap-6 pb-6'>
        <div className='min-w-[80px] w-[80px] h-[80px] bg-blue-500 rounded-md items-center'>img</div>
        <h2 className={`font-bold text-center text-[${getFontSize(team_name)}]`}>{team_name} </h2>
      </div>
        <div className='flex justify-center w-full'>
            <input className='min-w-[80px] w-1/2 h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary'/>
        </div>
    </div>
      <button 
        className='w-full p-3 mt-6 rounded-md bg-primary'
        onClick={handleSumbitClicked}
      >
        Submit Score
      </button>      
    </div>
  )
}

export default InCompetition_team