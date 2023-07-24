import  {useEffect, useState} from 'react'
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

import SignUp from './components/login_page/SignUp';
import Navbar from './components/navbar/Navbar';
import StartLeague from './components/create_league_page/StartLeague';
import Brolympics from './components/brolympics/Brolympics';
import League from './components/brolympics/League';
import Leagues from './components/brolympics/Leagues';
import VerifyPhone from './components/login_page/VerifyPhone';
import Invites from './components/invites/Invites';
import Team from './components/brolympics/team/Team.js';
import Events from './components/brolympics/events/Events.js';
import Home from './components/brolympics/home/Home.js';

import {fetchLeagues} from './api/fetchLeague.js'
import BrolympicsSettings from './components/league_settings/BrolympicsSettings.js';
import LeagueSettings from './components/league_settings/LeagueSettings.js';

function App() {
    const [leagues, setLeagues] = useState([])

    useEffect(()=> {
        const getLeagues = async () => {
            const response = await fetchLeagues()
            if (response.ok){
                const data = await response.json()
                setLeagues(data)
            } 
        }
        getLeagues()
    },[])

  return (
    <div className='min-h-screen bg-offWhite text-neutralDark'>
      <AuthProvider>
        <Navbar leagues={leagues}/>
        <Routes>
          <Route path='/sign-up/*' element={<SignUp/>}/>
          <Route path='/sign-up/verify' element={<VerifyPhone/>}/>
          <Route path='/start-league' element={<StartLeague/>}/>
          <Route path='/' element={<Leagues leagues={leagues}/>}/>
          <Route path='/league/:uuid' element={<League/>}/>
          <Route path='/league/settings/:uuid'  element={<LeagueSettings/>}/>
          <Route path='/b/:uuid/*' element={<Brolympics/>}></Route>
          <Route path='/invite/*' element={<Invites/>}/>
        </Routes>
      </AuthProvider>
    </div>
  )
  //eventually make league /l/<id> and brolympics /l/<id>/b/<id>
}

export default App
