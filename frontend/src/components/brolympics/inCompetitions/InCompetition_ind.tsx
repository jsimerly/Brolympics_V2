import { useState } from 'react'

const InCompetition_ind = ({team_name, player_1_name, player_2_name, name, decimal_places, max_score, min_score}) => {
    const [player1Score, setPlayerScore] = useState(0)
    const [player2Score, setPlayer2Score] = useState(0)

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
        if (isValidScore(player1Score) && isValidScore(player2Score)){
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
      <div className=''>
        <div className=''>
          <div className='flex items-center justify-start flex-1 gap-3'>
            <h4 
              className={
                `w-full py-2 text-start text-[30px]`}
            >{player_1_name}</h4>
            <div className='flex justify-center w-1/2'>
              <input className='min-w-[80px] w-[80px] h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary'/>
            </div>
          </div>
          <div className='py-6'/>
          <div className='flex items-center justify-start flex-1 gap-3'>
            <h4 
              className={
                `w-full py-2 text-start text-[30px]`}
            >{player_2_name}</h4>
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

export default InCompetition_ind