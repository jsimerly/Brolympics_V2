import {useState} from 'react'
import CloseIcon from '@mui/icons-material/Close';
import EditIcon from '@mui/icons-material/Edit';
import RemoveIcon from '@mui/icons-material/Remove';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import CopyWrapper from '../../Util/CopyWrapper';


const TeamCard = ({name, player_1, player_2}) => {
    const [editing, setEditing] = useState(false)
    const toggleEditing = () => {
        setEditing(editing => !editing)
    }    
    
    const onRemovePlayer = (player) => {
        console.log(player)
    }

    return(
        <div className='relative flex items-center gap-3 p-2 border rounded-md border-primary'>
            <div className={`relative ${editing ? 'min-[80px] w-[80px] h-[80px]' : 'min-w-[60px] w-[60px] h-[60px]'} rounded-md`}>
                <img className={`w-full h-full bg-white rounded-md  ${editing ? 'min-w-[80px] h-[80px]' : 'min-w-[60px] h-[60px]'} `}/>
                {editing &&
                    <CameraAltIcon sx={{fontSize:40}} className='absolute z-20 w-full h-full transform -translate-x-1/2 -translate-y-1/2 text-neutral opacity-30 top-1/2 left-1/2'/>
                }
            </div>
            <div className='flex items-center justify-between w-full'>
                <div>
                    <h3 className='font-bold'>{name}</h3>
                    <div className='text-[16px]'>
                        {editing ? 
                            <div className='flex flex-col'>
                                <div
                                    onClick={()=>onRemovePlayer(player_1)}
                                >
                                    <RemoveIcon className='text-errorRed' sx={{fontSize:20}}/>
                                    {player_1}
                                </div>
                                <div
                                    onClick={()=>onRemovePlayer(player_2)}
                                >
                                    <RemoveIcon className='text-errorRed' sx={{fontSize:20}}/>
                                    {player_2}
                                </div>
                            </div>

                            :
                            <div>
                                {player_1} {player_1 && player_2 && ' & '} {player_2}
                            </div>
                        }
                    </div>
                </div>
                <button 
                    className='absolute flex right-2 top-2'
                    onClick={toggleEditing}
                >
                    {editing ?
                        <CloseIcon sx={{fontSize:20}}/>
                        :
                        <EditIcon sx={{fontSize:20}}/>
                    }
                </button>
                {editing &&
                    <button className='p-1 px-2 text-white rounded-md bg-errorRed text-[12px] mt-3 absolute bottom-2 right-2'>
                        Delete Team
                    </button>
                }
                {!editing && !(player_1 && player_2) &&
                    <div className='absolute bottom-2 right-2 text-primary text-[12px] border-primary border p-1 rounded-md flex items-center gap-1'>
                        <CopyWrapper
                            copyString={'This is text to copy'}
                            size={20}
                        >
                            <span className='mr-1'>Copy Invite Link</span>
                        </CopyWrapper>
                    </div>
                }
            </div>
        </div>
    )
}



const ManageTeams = () => {
    const teams = [
        {'name' : 'El Salvador', 'player_1' : "Jacob", 'player_2': 'Javi'},
        {'name' : 'Great Britian', 'player_1' : "Noah", 'player_2': 'Anthony'},
        {'name' : 'Greece', 'player_1' : "Timmy", 'player_2': null},
    ]

  return (
    <div className=''>
        <h2 className='font-semibold text-[20px]'>Manage Teams</h2>
        <div className='my-2 space-y-3'>
            {teams.map((team,i) => (
                <TeamCard {...team}/>
            ))}
        </div>
        <div>Create Team</div>
    </div>
  )
}

export default ManageTeams