import {useState} from 'react'
import { useNavigate, useLocation, useParams } from 'react-router-dom'
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import PeopleAltOutlinedIcon from '@mui/icons-material/PeopleAltOutlined';
import EmojiEventsOutlinedIcon from '@mui/icons-material/EmojiEventsOutlined';
import ScoreboardOutlinedIcon from '@mui/icons-material/ScoreboardOutlined';
import SettingsSuggestIcon from '@mui/icons-material/SettingsSuggest';

const Toolbar = ({is_owner}) => {
    const navigate = useNavigate();
    const {pathname} = useLocation()
    const pathAfterBrolympics = pathname.split("/")[3];
    const [currentPage, setCurrentPage] = useState(pathAfterBrolympics)
    const {uuid} = useParams()

    const handleIconClick = (route) => {
        setCurrentPage(route)
        navigate(`/b/${uuid}/${route}`)
    }

    const PageButton = ({route, text, icon}) => (
        <div 
            onClick={() => handleIconClick(route)}
            className={`${currentPage === route && 'text-primary'} flex flex-col items-center justify-center flex-1`}
        >
        {icon}
        <span className='text-[10px]'>{text}</span>
    </div>
    )

  return (
    <>
        <div className='h-[60px] -z-10'/>
        <div className='fixed bottom-0 left-0 h-[60px] bg-neutral w-full border-t border-neutralLight flex justify-around items-center px-3'>
            <PageButton 
                route='home' text='Home' 
                icon={<HomeOutlinedIcon sx={{fontSize:30}}/>}
            />
            <PageButton 
                route='team' text='Team' 
                icon={<PeopleAltOutlinedIcon sx={{fontSize:30}}/>}
            />
            <PageButton 
                route='event' text='Events' 
                icon={<ScoreboardOutlinedIcon sx={{fontSize:30}}/>}
            />
            <PageButton 
                route='standings' text='Standings' 
                icon={<EmojiEventsOutlinedIcon sx={{fontSize:30}}/>}
            />
            {is_owner &&
                <PageButton 
                    route='manage' text='Manage' 
                    icon={<SettingsSuggestIcon sx={{fontSize:30}}/>}
                />
            }
        </div>
    </>

  )
}

export default Toolbar