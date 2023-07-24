import { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation, useParams} from "react-router-dom"

import EditBracket from "./EditBracket"
import EditComp from "./EditComp"
import EditEvent from "./EditEvent"
import EditOverall from "./EditOverall"
import ManageBro from "./ManageBro"
import ManageEvents from "./ManageEvents"
import ManageTeams from "./ManageTeams"
import Manage from './Manage';

const ManageRouter = () => {
  return (
    <div className='min-h-[calc(100vh-220px)] h-full bg-offWhite text-neutralDark'>
        <Routes>
            <Route path='/' element={<Manage/>}/>
            <Route path='edit-bracket' element={<EditBracket/>}/>
            <Route path='edit-competition' element={<EditComp/>}/>
            <Route path='edit-event' element={<EditEvent/>}/>
            <Route path='edit-overall' element={<EditOverall/>}/>
            <Route path='manage-brolympics' element={<ManageBro/>}/>
            <Route path='manage-teams' element={<ManageTeams/>}/>
            <Route path='manage-events' element={<ManageEvents/>}/>
        </Routes>
    </div>
  )
}

export default ManageRouter