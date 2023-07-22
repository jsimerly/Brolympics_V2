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

function App() {

  return (
    <div className='min-h-screen bg-offWhite text-neutralDark'>
      <AuthProvider>
        <Navbar/>
        <Routes>
          <Route path='/sign-up/*' element={<SignUp/>}/>
          <Route path='/sign-up/verify' element={<VerifyPhone/>}/>
          <Route path='/start-league' element={<StartLeague/>}/>
          <Route path='/' element={<Leagues/>}/>
          <Route path='/league' element={<League/>}/>
          <Route path='/brolympics/*' element={<Brolympics/>}/>
        </Routes>
      </AuthProvider>
    </div>
  )
  //eventually make league /l/<id> and brolympics /l/<id>/b/<id>
}

export default App
