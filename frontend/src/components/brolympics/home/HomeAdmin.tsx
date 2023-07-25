import {useState} from 'react'
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import ContentCopyOutlinedIcon from '@mui/icons-material/ContentCopyOutlined';
import ManageBro from '../manage/ManageBro';
import ManageEvents from '../manage/ManageEvents';
import ManageTeams from '../manage/ManageTeams';


const HomeAdmin = () => {
  const [copySuccess, setCopySuccess] = useState(false);
  const [cropping, setCropping] = useState(false)
  
  const handleImageUpload = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
        const file = e.target.files[0];
        let imageDataUrl = await readImageFile(file);
        
        setLeagueData(prevLeague => ({...prevLeague, img: file, imgSrc: imageDataUrl }));
        setCropping(true);
    }
  };


  const copyToClipboard = async (text) => {
    if (!navigator.clipboard) {
      // Clipboard API not available
      return;
    }
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(true);
      setTimeout(() => {
        setCopySuccess(false);
      }, 3000);
    } catch (err) {
      console.log('Could not copy.')
    }
  }
  
  return (
    <div className='min-h-[calc(100vh-220px)] bg-offWhite text-neutralDark p-6 flex flex-col gap-3'>
      <div className='w-full p-3 border rounded-md border-primary'>
        <h3 className='w-full font-semibold text-center'>Ready to Go?</h3>
        <div className='flex items-center justify-center w-full mt-3'>
          <button className='w-1/2 p-2 font-bold text-white rounded-md bg-primary'>
            Start Brolympics
          </button>
        </div>
        
      </div>
      <h3 className='flex items-center w-full gap-3 text-errorRed'>
          <PriorityHighIcon/> 
          <span className='text-[12px]'>Make sure you fully update all of your event settings before your Brolympics begins.</span>
      </h3>
      <ManageEvents/>
      <ManageTeams/>



      <ManageBro/>
    </div>
  )
}

export default HomeAdmin