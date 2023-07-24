import DataList from './DataList';
import {useNavigate} from 'react-router-dom'

const Card = (info, index, setOpen) => {
    const navigate = useNavigate()
    const onClick = () => {
      navigate(`/b/${info.uuid}`)
      setOpen(false)
    }
    
    return(
        <div 
            className='flex items-center w-full gap-3 p-3 rounded-md fex-items-center' 
            key={index}
            onClick={onClick}
        > 
            <div className='bg-white h-[40px] w-[40px] rounded-lg text-black'>
                logo
            </div>
            <div className="flex flex-col">
                <h3 className="text-[18px]">{info.name}</h3>
                <div className='text-[14px] ml-1 opacity-60'>
                    Rank: 1st Points: 36.5
                </div>
            </div>
        </div>
    );
}



const CurrentBrolympics = ({current_brolympics, setOpen}) => {

    return (
        <>
        {
            current_brolympics.length !== 0 &&
            <DataList
                title="Current Brolympics"
                data={current_brolympics}
                card={Card}
                setOpen={setOpen}
            /> 
        }
        </>
    )
}

export default CurrentBrolympics;