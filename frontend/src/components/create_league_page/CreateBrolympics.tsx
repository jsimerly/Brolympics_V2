import { useState } from 'react';
import CreateWrapper from './CreateWrapper'
import CameraAltIcon from '@mui/icons-material/CameraAlt';

const CreateBrolympics = ({step, nextStep}) => {
    const [brolympicsName, setBrolympicsName] = useState()
    const [brolympicsImage, setBrolympicsImage] = useState()
    const [estStartDate, setEstStartDate] = useState()
    
    
    const handleCreateClicked = () => {
        console.log('CREATE Brolmpycs')
        nextStep()
    }

    const handleImageUpload = (event) => {
        setBrolympicsImage(event.target.files[0]);
    }

  return (
    <CreateWrapper
        button_text={'Create Brolympics'}
        step={step}
        submit={handleCreateClicked}
        title={'Create a Brolympics'}
        description={'A Brolympics is a group of events and competitions that are battled out between teams of 2. Utilmately at the end there is only 1 winner.'}
    >
        <div className='flex flex-col w-full gap-3'>
            <div>
                <h3 className='ml-1'>Name *</h3>
                <input 
                    type='text' 
                    value={brolympicsName} 
                    onChange={(e) => setBrolympicsName(e.target.value)}
                    placeholder='Ex: Summer 2023'
                    className='w-full p-2 border border-gray-200 rounded-md'
                />
            </div>
            <div>
                <h3 className='ml-1'>Start Date <span className='text-[12px]'> (Optional)</span></h3>
                <input 
                    type='date' 
                    value={brolympicsName} 
                    onChange={(e) => setEstStartDate(e.target.value)}
                    className='w-full p-2 border border-gray-200 rounded-md'
                />
            </div>
            <div>
                <h3 className='ml-1'>Upload a Logo <span className='text-[12px]'> (Optional)</span></h3>    
                <input 
                        type='file' 
                        accept="image/*"
                        id='file' 
                        onChange={handleImageUpload}
                        hidden      
                    />
                <label 
                    htmlFor='file'  
                    className='inline-flex p-4 bg-white border border-gray-200 rounded-md cursor-pointer'
                >
                    <CameraAltIcon className='bg-white text-neutral' sx={{fontSize:40}}/>
                </label>
            </div>
        </div>
    </CreateWrapper>
  )
}

export default CreateBrolympics