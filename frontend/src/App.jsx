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

import {fetchLeagues} from './api/fetchLeague.js'
import Notification, { useNotification } from './components/Util/Notification.jsx';


function App() {
    const [leagues, setLeagues] = useState([])
    const { notification, setNotification } = useNotification()

    useEffect(()=> {
        const getLeagues = async () => {
            const response = await fetchLeagues()
            if (response.ok){
                const data = await response.json()
                setLeagues(data)
                console.log(data)
            } 
        }
        getLeagues()
    },[])

  return (
    <div className='min-h-screen text-white bg-neutral'>
        <AuthProvider>
          <Navbar leagues={leagues}/>
          {notification.show &&
            <Notification
              message={notification.message}
              className={notification.className}
              onClose={() => setNotification({ ...notification, show: false })}
            />
          }
          <Routes>
            <Route path='/sign-up/*' element={<SignUp/>}/>
            <Route path='/sign-up/verify' element={<VerifyPhone/>}/>
            <Route path='/start-league' element={<StartLeague/>}/>
            <Route path='/' element={<Leagues leagues={leagues}/>}/>
            <Route path='/league/:uuid' element={<League/>}/>
            <Route path='/b/:uuid/*' element={<Brolympics/>}></Route>
            <Route path='/invite/*' element={<Invites/>}/>
          </Routes>
        </AuthProvider>
    </div>
  )
}

export default App
