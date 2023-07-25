

import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../../context/AuthContext'

import CurrentBrolympics from "./CurrentBrolympics"
import LeaguesButtons from "./LeaguesButtons"
import Options from "./Options"
import UpcomingBrolympics from "./UpcomingBrolympics"
import UpcomingCompetitions from "./UpcomingComps"
import Account from './Account';
import {fetchUpcoming} from '../../api/fetchLeague.js'

const Slideout = ({open, leagues, setOpen}) => {
    const [view, setView] = useState('leagues')
    const {currentUser} = useContext(AuthContext)

    const [currentBro, setCurrentBro] = useState([])
    const [upcomingBro, setUpcomingBro] = useState([])
    const [upcomingComps, setUpcomingComps] = useState([])

    useEffect(() => {
        const getInfo = async () => {
            const response = await fetchUpcoming()

            if (response.ok){
                const data = await response.json()
                setCurrentBro(data['current_brolympics'])
                setUpcomingBro(data['upcoming_brolympics'])
                setUpcomingComps(data['upcoming_competitions'])
            } else {
                console.log('error')
            }
        }
        getInfo()
    },[])
    

    useEffect(() => {

    },[currentUser])


  return (
    <>
        {open &&
            <div className="fixed top-[80px] left-0 w-full z-30">
                {view === 'account' ?
                    <Account setView={setView}/>
                :
                    <div className='flex flex-col h-[calc(100vh-80px)] bg-neutral text-white opacity-[99%] px-6 py-3 gap-3'>
                        <LeaguesButtons leagues={leagues} setOpen={setOpen}/>
                        <CurrentBrolympics current_brolympics={currentBro} setOpen={setOpen}/>
                        <UpcomingBrolympics upcoming_brolympics={upcomingBro} setOpen={setOpen}/>
                        <UpcomingCompetitions upcoming_competitions={upcomingComps} setOpen={setOpen}/>                        
                    </div>
                }

                <div>
                    <Options currentUser={currentUser} setView={setView}/>
                </div>
            </div>
        }
    </>
  )
}

export default Slideout