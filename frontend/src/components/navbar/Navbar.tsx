import {useState} from 'react'
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import Slideout from './Slideout';

const Navbar = ({leagues}) => {
    const [slideOpen, setSlideOpen]= useState(false)

    const menuClick = () => {
        setSlideOpen(prevState => !prevState);
      };

  return (
    <>
        <div className='fixed h-[80px] z-20 bg-neutralDark text-offWhite w-full flex justify-between items-center px-3'>
            <div 
                className=''
                onClick={menuClick}
            >
                {slideOpen ?<CloseIcon sx={{fontSize: 35}}/> : <MenuIcon sx={{fontSize: 35}}/>}   
             
            </div>
            <div>
                Logo
            </div>
        </div>
        <div className='h-[80px]'/>
        <Slideout 
            leagues={leagues}
            open={slideOpen}
        />
    </>

  )
}

export default Navbar