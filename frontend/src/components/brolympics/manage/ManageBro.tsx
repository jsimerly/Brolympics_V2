import {useState} from 'react'
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import ContentCopyOutlinedIcon from '@mui/icons-material/ContentCopyOutlined';
import ImageCropper, {readImageFile} from '../..//Util/ImageCropper';
import CameraAltIcon from '@mui/icons-material/CameraAlt';

const ManageBro = () => {
    const [copySuccess, setCopySuccess] = useState(false);
    const [cropping, setCropping] = useState(false)
    const [broData, setBroData] = useState()

    const handleImageUpload = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            let imageDataUrl = await readImageFile(file);
            
            //set the brolypmics data
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

      const setCroppedImage = (croppedImage) => {
        setBroData(prevData => ({...prevData, img: croppedImage}))
        setCropping(false)
    }
  return (
    <div>
        <h2 className='font-semibold text-[20px]'>
          Manage Brolympics          
        </h2>
        <div>        
        <div className='w-full py-3'>
          <span className='ml-1 text-[12px]'>Name</span>
          <input
            className='w-full p-2 border rounded-md border-primary'
          />
        </div>
        <div>
        <h3 className='ml-1'>
            Upload a Logo <span className='text-[12px]'> (Optional)</span>
        </h3>    
            <input 
                    type='file' 
                    accept="image/*"
                    id='file_bro' 
                    onChange={handleImageUpload}
                    hidden      
                />
            <label 
                htmlFor='file_bro'  
                className='inline-flex bg-white border border-gray-200 rounded-md cursor-pointer'
            >
                { broData && broData.img ?
                    <img src={broData.img} className='max-w-[100px] rounded-md'/>
                    :
                    <div className='w-[100px] h-[100px] rounded-md flex items-center justify-center'>
                        <CameraAltIcon className='bg-white w-[100px] text-neutral' sx={{fontSize:60}}/>
                    </div>
                }
            </label>
            {cropping &&
                <ImageCropper 
                    img={broData.imgSrc} 
                    setCroppedImage={setCroppedImage}
                />
            }
        </div>
        <div className='flex flex-col w-full gap-3 mt-3'>
          <div className='flex flex-col'>
            <span className='ml-1 text-[12px]'>Start Date</span>
            <input 
              className='flex w-full p-2 border rounded-md border-primary'
              type='datetime-local'
            />
          </div>
          <div className='flex flex-col'>
            <span className='ml-1 text-[12px]'>End Date</span>
            <input 
              className='flex w-full p-2 border rounded-md border-primary'
              type='datetime-local'
            />
          </div>
        </div>
        <div className='mt-3'>
        <h4 className='pb-1 font-bold'>Copy the Link and Share with Friends</h4>
          <div 
            className='flex justify-between p-2 bg-white border rounded-md'
            onClick={()=>copyToClipboard('https://sleeper.com/i/k7N5Yxx00Ywz')}
          >
            https://sleeper.com/i/k7N5Yxx00Ywz
            <ContentCopyOutlinedIcon className='text-primary'/>
          </div>
          {copySuccess && <div className='text-primary'>Copied!</div>}
        </div>
      </div>
      <button className='w-full p-2 mt-6 font-semibold text-white rounded-md bg-primary'>
        Update Brolympics
      </button>
      <div>
        <h4 className='pt-6 text-[16px] font-semibold'>
            Danger Zone
        </h4>
        <button className='w-full p-2 mt-6 font-semibold text-white rounded-md bg-errorRed'>
            Delete Brolympics
        </button>
      </div>
    </div>
  )
}

export default ManageBro