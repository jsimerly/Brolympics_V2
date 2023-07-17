import  {useEffect, useState} from 'react'
import { Routes, Route } from 'react-router-dom';

import SignUp from './components/login_page/SignUp';
import Navbar from './components/navbar/Navbar';
import StartLeague from './components/create_league_page/StartLeague';

function App() {

  return (
    <div className='min-h-screen bg-offWhite text-neutralDark'>
      <Navbar/>
      <Routes>
        <Route path='/sign-up' element={<SignUp/>}/>
        <Route path='/start-league' element={<StartLeague/>}/>
      </Routes>
    </div>
  )
}

export default App
