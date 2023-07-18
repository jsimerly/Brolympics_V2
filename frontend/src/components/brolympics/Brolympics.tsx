import { useEffect } from 'react';
import { Routes, Route, Navigate } from "react-router-dom"
import Toolbar from "./toolbar/Toolbar"
import Events from "./events/Events"
import Standings from "./standings/Standings"
import Home from "./home/Home"
import Team from "./team/Team"

const Brolympics = () => {

  return (
    <div className='bg-neutral min-h-[calc(100vh-80px)] text-white'>
      <div className='w-full p-3 text-center border-b border-neutralLight'>
        <h1 className='w-full font-bold leading-none text-[30px] '>
          Summer 2023
        </h1>
        <span>Stuck in Highschool</span>
      </div>
        <Routes>
            <Route path="/home" element={<Home />} />
            <Route path="/standings" element={<Standings />} />
            <Route path="/team" element={<Team />} />
            <Route path="/team/:teamName" element={<Team />} />
            <Route path="/events" element={<Events />} />
            <Route path="/events:/eventName" element={<Events />} />
            <Route 
                path="*" 
                element={<Navigate to="home" replace/>} 
            />
        </Routes>
        <Toolbar/>
    </div>
  )
}

export default Brolympics