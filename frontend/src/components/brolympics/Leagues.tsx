import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import CloseIcon from '@mui/icons-material/Close';

const LeagueCard = ({name, img, founded_date}) => {    
    return (
        <div className='flex px-3 py-6 '>
            <div className='bg-white h-[60px] min-w-[60px] w-[60px] rounded-md'>
                logo
            </div>
            <div className='flex flex-col items-center justify-center w-full'>
                <h2 className='text-[30px] font-bold w-full text-center'> {name}</h2>
                <span className=' text-center text-[14px]'>Founded: {founded_date}</span>
            </div>
        </div>
    )
}


const Leagues = () => {
    const [leagueName, setLeagueName] = useState()
    const [open, setOpen] = useState(false)
    const leagues = [
        {
            'name' : "Jacob's League",
            'founded_date' : '2014',
            'league_id' : '1234353'
        },
    ]

    const navigate = useNavigate()

    const createLeagueClicked = () => {
        navigate('/start-league')
    }

    // const openCreate = () => {
    //     setOpen(true)
    // }

    // const closeCreate = () => {
    //     setOpen(false)
    // }
    
    
    // const CreateLeaguePopup = () => (
    //     <div className='fixed inset-0 flex items-center justify-center p-6'>
    //         <div className='w-full p-6 border rounded-md border-primary'>
    //             <div className='flex justify-between w-full'>
    //                 <h3 className='font-bold text-[20px]'>Create League</h3>
    //                 <CloseIcon onClick={closeCreate}/>
    //             </div>
    //             <input 
    //                 className='w-full text-[20px] p-2 rounded-md bg-neutralLight my-3'
    //                 placeholder='League Name'
    //             />
    //             <button className='w-full p-3 font-bold rounded-md bg-primary'>
    //                 Create
    //             </button>
    //         </div>
    //     </div>
    // )
   
     

  return (
    <div className='bg-neutral relative text-white min-h-[calc(100vh-80px)]'>
        <div className='p-6'>
            <h1 className='text-[26px] font-bold leading-none py-3'>Leagues</h1>
            {leagues.map((league, i) => (
                <div key={i}>
                    <LeagueCard {...league}/>
                    {i !== 0 && <div className='w-full h-[1px] bg-neutralLight'/>}
                </div>
            ))}
            {leagues.length === 0 && 'You are not in any leagues yet.'}
        </div>


        <div className='fixed bottom-0 left-0 flex justify-between w-screen p-6 '>
            <button 
                className='flex justify-between w-full p-3 px-6 rounded-md bg-primary'
                onClick={createLeagueClicked}
            >
                <AddCircleOutlineIcon/>
                <span> Create League </span>
                <div/> 
            </button>
        </div>
    </div>
  )
}

export default Leagues