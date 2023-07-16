import  {useEffect, useState} from 'react'
import { Routes, Route } from 'react-router-dom';

import SignUp from './components/login_page/SignUp';
import Navbar from './components/navbar/Navbar';

function App() {

  return (
    <div className='bg-offWhite'>
      <Navbar/>
      <Routes>
        <Route path='/sign-up' element={<SignUp/>}/>
      </Routes>
    </div>
  )
}

export default App
