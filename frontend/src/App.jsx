import  {useEffect, useState} from 'react'
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.jsx';

import SignUp from './components/login_page/SignUp.jsx';
import Navbar from './components/navbar/Navbar.jsx';
import StartLeague from './components/create_league_page/StartLeague.jsx';
import Brolympics from './components/brolympics/Brolympics.jsx';
import League from './components/brolympics/League.jsx';
import Leagues from './components/brolympics/Leagues.jsx';
import VerifyPhone from './components/login_page/VerifyPhone.jsx';
import Invites from './components/invites/Invites.jsx';
import Team from './components/brolympics/team/Team.jsx';
import Events from './components/brolympics/events/Events.jsx';
import Home from './components/brolympics/home/Home.jsx';

import {fetchLeagues} from './api/fetchLeague.js'
import BrolympicsSettings from './components/league_settings/BrolympicsSettings.jsx';
import LeagueSettings from './components/league_settings/LeagueSettings.jsx';

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
