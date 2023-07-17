
import {useState} from 'react'
import CreateWrapper from "./CreateWrapper"
import CameraAltIcon from '@mui/icons-material/CameraAlt';

const CreateLeaguePage = ({step, nextStep}) => {
    const [leagueName, setLeagueName] = useState()
    const [leagueImageFile, setLeagueImageFile] = useState()

    const handleCreateClicked = () => {
        console.log('CREATE LEAGUE')
        nextStep()
    }

    const handleImageUpload = (event) => {
        setLeagueImageFile(event.target.files[0]);
    }

  return (
    <CreateWrapper
        button_text={'Create League'}
        step={step}
        submit={handleCreateClicked}
        title={'Create Your League'}
        description={'A league is a collection of brolympics where you can keep track of historical brolympics winners, events, teams, and even player performances.'}
    >
        <div className='flex flex-col w-full gap-3'>
            <div>
                <h3 className='ml-1'>Name *</h3>
                <input 
                    type='text' 
                    value={leagueName} 
                    onChange={(e) => setLeagueName(e.target.value)}
                    placeholder='Enter the name of your league'
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

export default CreateLeaguePage