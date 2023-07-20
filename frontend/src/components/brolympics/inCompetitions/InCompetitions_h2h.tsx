import { useState } from 'react'

const InCompetitions_h2h = ({team_1_name,  team_2_name, name, decimal_places, max_score, min_score}) => {
    const [team1Score, setTeam1Score] = useState(0)
    const [team2Score, setTeam2Score] = useState(0)
  
  const getFontSize = (name) => {
    if (name) {
      if (name.length <= 10) {
          return '30px';
      } else if (name.length <= 16) {
          return '26px';
      } else if (name.length <= 20) {
          return '20px';
      } else {
          return '16px'
      }
    }
  }

  const isValidScore = (score) => {
    return score >= min_score && score <= max_score
  }

  const handleSumbitClicked = () => {
    if (isValidScore(team1Score) && isValidScore(team2Score)){
      console.log(1)
    }
  }

  return (
    <div className='min-h-[calc(100vh-160px)] flex flex-col justify-between p-6'>
      <div>
      <h2 className=' w-full text-center text-[20px] mb-3'>
       {name}
      </h2>
      <div className=''>
        <div className=''>
          <div className='flex items-center justify-start flex-1 gap-3'>
            <div className='min-w-[80px] w-[80px] h-[80px] bg-blue-500 rounded-md items-center'>img</div>
            <h4 
              className={
                `w-full py-2 font-bold text-start
                text-[${getFontSize(team_1_name)}]
                `}
            >{team_1_name}</h4>
            <div className='flex justify-center w-1/2'>
              <input className='min-w-[80px] w-[80px] h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary'/>
            </div>
          </div>
          <div className='py-6'/>
          <div className='flex items-center justify-start flex-1 gap-3'>

            <h4 
              className={
                `w-full py-2 font-bold text-start
                text-[${getFontSize(team_2_name)}]
                `}
            >{team_2_name}</h4>
            <div className='flex justify-center w-1/2'>
              <input className='min-w-[80px] w-[80px] h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary'/>
            </div>
          </div>
        </div>
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
export default InCompetitions_h2h