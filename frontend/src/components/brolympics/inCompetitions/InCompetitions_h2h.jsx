import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { fetchActiveComp_h2h, fetchSubmitComp_h2h} from '../../../api/activeBro/fetchHome'

const InCompetitions_h2h = ({}) => {
    const [team1Score, setTeam1Score] = useState(0)
    const [team2Score, setTeam2Score] = useState(0)
    const handleTeam1ScoreChange = (e) => setTeam1Score(e.target.value);
    const handleTeam2ScoreChange = (e) => setTeam2Score(e.target.value);
  
    const {compUuid} = useParams()

    const [compData, setCompData] = useState()
    useEffect(()=>{
      const getData = async () => {
        const response = await fetchActiveComp_h2h(compUuid)

        if (response.ok){
          const data = await response.json()
          setCompData(data)
          console.log(data)
        }
      }
      getData()
      
    },[])

    
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
    const minScore = compData.min_score === null ? -Infinity : compData.min_score;
    const maxScore = compData.max_score === null ? Infinity : compData.max_score;
    
    return score >= minScore && score <= maxScore;
  }

  const handleSumbitClicked = async () => {
    if (isValidScore(team1Score) && isValidScore(team2Score)){
      const response = await fetchSubmitComp_h2h(compUuid, team1Score, team2Score)
      if (response.ok){
        location.reload()
      }
    }
  }

  return (
    compData &&
    <div className='min-h-[calc(100vh-240px)] p-6 flex-col flex justify-between'>
          <div>
          <h2 className=' w-full text-center text-[20px] mb-3 font-semibold'>
            {compData.event}
          </h2>
          <div className=''>
            <div className=''>
              <div className='flex items-center justify-start flex-1 gap-3'>
                <img src={compData.team_1.img} className='min-w-[80px] w-[80px] h-[80px] bg-blue-500 rounded-md items-center'/>
                <h4 
                  className={
                    `w-full py-2 font-bold text-start
                    text-[${getFontSize(compData.team_1.name)}]
                    `}
                >{compData.team_1.name}</h4>
                <div className='flex justify-center w-1/2'>
                  <input 
                    value={team1Score || ''}
                    onChange={handleTeam1ScoreChange}
                    className='min-w-[80px] w-[80px] h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary text-center text-[20px] font-semibold'
                  />
                </div>
              </div>
              <div className='py-6'/>
              <div className='flex items-center justify-start flex-1 gap-3'>
              <img src={compData.team_2.img} className='min-w-[80px] w-[80px] h-[80px] bg-blue-500 rounded-md items-center'/>
                <h4 
                  className={
                    `w-full py-2 font-bold text-start
                    text-[${getFontSize(compData.team_2.name)}]
                    `}
                >{compData.team_2.name}</h4>
                <div className='flex justify-center w-1/2'>
                  <input 
                    value={team2Score || ''}
                    onChange={handleTeam2ScoreChange}
                    className='min-w-[80px] w-[80px] h-[60px] p-2 mx-6 rounded-md bg-neutralLight border outline-primary text-center text-[20px] font-semibold'
                  />
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