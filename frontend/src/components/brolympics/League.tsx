import Gold from '../../assets/svgs/gold.svg'
import Silver from '../../assets/svgs/silver.svg'
import Bronze from '../../assets/svgs/bronze.svg'
import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import {fetchLeagueInfo} from '../../api/fetchLeague.js'


const BrolympicsCard_Upcoming = ({img, name, events, teams, projected_start_date, uuid}) => {
    const navigate = useNavigate()
    const handleGoToBrolympics = () => {
        navigate(`/b/${uuid}/home/`)
    }

    return(
        <div 
            className='p-3 border rounded-md border-primary'
            onClick={handleGoToBrolympics}
        >
            <div className="flex items-center justify-between">
                <div className="flex gap-3 item-center">
                    <img src={img}className='bg-white h-[80px] w-[80px] rounded-lg text-black'/>
                    <div className='flex flex-col justify-center'>
                        <h3 className="text-[20px] font-bold flex items-center">{name}</h3> 
                        <div className="text-[12px] flex items-start justify-start">
                            {projected_start_date &&
                                <span>{projected_start_date}</span>
                            }
                        </div>
                    </div>
                </div>
            </div>
            <div className="flex pt-6 text-[14px]">
                <div className="pr-2 text-[16px] flex items-center justify-center">
                    Events:
                </div>
                <div className="flex flex-wrap gap-2">
                    {events.map((event, i) => (
                        <div className='p-1 border rounded-md border-primaryLight'>
                            {event.name}
                        </div>
                    ))}
                </div>
            </div>
            { teams.length > 0 &&
                <div className="flex pt-3 text-[14px]">
                    <div className="pr-2 text-[16px]">
                        Teams:
                    </div>
                </div>
            }
        </div>
    )
}



const BrolympicsCard_Completed = ({img, name, end_date, winner, second, third}) => (
    <div className='p-3 border rounded-md border-primary'>
        <div className="flex items-center justify-between">
            <div className="flex gap-3 item-center">
                <img src={img}className='bg-white h-[80px] w-[80px] rounded-lg text-black'/>
                <h3 className="text-[20px] font-bold flex items-center">{name}</h3>
            </div>
            <div className="text-[12px] flex items-end justify-end">
                {end_date}
            </div>
        </div>
        <div className='flex flex-col justify-center gap-3 px-2 pt-4'>
            <div className='flex gap-1'>
                <img src={Gold} className='h-[20px]'/>
                {winner}
            </div>
            <div className='flex gap-1'>
                <img src={Silver} className='h-[20px]'/>
                {second}
            </div>
            <div className='flex gap-1'>
                <img src={Bronze} className='h-[20px]'/>
                {third}
            </div>
        </div>
    </div>
)

const League = () => {
    const [leagueInfo, setLeagueInfo] = useState()
    const {uuid} = useParams()
    
    useEffect(() => {
       const getLeagueInfo = async () => {
        const response = await fetchLeagueInfo(uuid)
        
        if (response.ok){
            const data = await response.json()
            setLeagueInfo(data)
        } else {
            const data = await response.json()
            console.log('error')
        }
       } 
       getLeagueInfo()
    },[])


  return (
    <div className='min-h-[calc(100vh-80px)] px-6 py-3 text-white bg-neutral'>
        <div>
            <h1 className='text-[26px] font-bold leading-none pt-3'>
                Stuck in Highschool
            </h1>
            <span className='text-[12px]'>Founded: 2014</span>
        </div>
        <div>
            <h2 className="py-3 ml-1 font-bold"> Upcoming Brolympics </h2>
            <div className="flex flex-col gap-3">
                {leagueInfo &&
                    leagueInfo.upcoming_brolympics.map((brolympic, i) => (
                        <BrolympicsCard_Upcoming {...brolympic} key={i}/>
                    ))
                }
                {leagueInfo && leagueInfo.upcoming_brolympics.length === 0 && "You have do not have any upcoming Brolympics."}
            </div>
            <h2 className="py-3 ml-1 font-bold"> Completed Brolympics </h2>
            <div className="flex flex-col gap-3">
                {leagueInfo &&
                    leagueInfo.completed_brolympics.map((brolympic, i) => (
                        <BrolympicsCard_Completed {...brolympic} key={i}/>
                    ))
                }
                {leagueInfo && leagueInfo.completed_brolympics.length === 0 && "You have not completed any Brolympics."}
            </div>
        </div>
    </div>
  )
}

export default League