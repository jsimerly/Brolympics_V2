import {useState} from 'react'
import ImageCropper, {readImageFile} from '../../Util/ImageCropper';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import CopyWrapper from '../../Util/CopyWrapper';
import { fetchDeleteBrolympics } from '../../../api/fetchBrolympics';
import PopupContinue from '../../Util/PopupContinue';
import { useNavigate, useParams } from 'react-router-dom';
import { useNotification } from '../../Util/Notification';

const ManageBro = () => {
    const [cropping, setCropping] = useState(false)
    const [broData, setBroData] = useState()
    const navigate = useNavigate()
    const { showNotification } = useNotification()
    const {uuid} = useParams()

    const handleImageUpload = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            let imageDataUrl = await readImageFile(file);
            
            //set the brolypmics data
        }
      };

    
    const setCroppedImage = (croppedImage) => {
      setBroData(prevData => ({...prevData, img: croppedImage}))
      setCropping(false)
    }

    const [popupDelete, setPopupDelete] = useState(false)

    const onDeleteClicked = () => {
      setPopupDelete(true)
    }

    const deleteTeamFunc = async () => {
      const response = await fetchDeleteBrolympics(uuid)
      if (response.ok){
        showNotification('This brolympics has been deleted.', '!border-primary')
        navigate('/')
      } else {
        showNotification('There was an error when attempting to delete this brolympics')
      }
    }
    
  return (
    <div>
      <PopupContinue
        open={popupDelete}
        setOpen={setPopupDelete}
        header={"Delete this Brolympics?"}
        desc={"Deleting this will perminately delete this Brolympics and remove all players and data from it. This will not be able to be recovered. Would you like to continue?"}
        continueText={'Delete'}
        continueFunc={deleteTeamFunc}
      />
        <h2 className='font-bold text-[16px]'>
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
            className='flex p-2 bg-white border rounded-md'
          >
            <CopyWrapper copyString={'https://sleeper.com/i/k7N5Yxx00Ywz'}>
                <span className='flex flex-1'>https://sleeper.com/i/k7N5Yxx00Ywz</span>
            </CopyWrapper>
          </div>
        </div>
      </div>
      <button className='w-full p-2 mt-6 font-semibold text-white rounded-md bg-primary'>
        Update Brolympics
      </button>
      <div>
        <h4 className='pt-6 text-[16px] font-semibold'>
            Danger Zone
        </h4>
        <button 
          className='w-full p-2 mt-6 font-semibold text-white rounded-md bg-errorRed'
          onClick={onDeleteClicked}
        >
            Delete Brolympics
        </button>
      </div>
    </div>
  )
}

export default ManageBro