
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DataList from './DataList';

const LeaguesButtons = ({leagues}) => {
  const AddLeagueButton = () => (
    <div className='flex gap-3 p-3 text-[16px]'>
      Add League
      <AddCircleOutlineIcon/>
    </div>
  )
  const Card = (league_name, index) => (
    <div className='flex items-center w-full gap-3 p-3 rounded-md'> 
      <div className='bg-white h-[40px] w-[40px] rounded-lg text-black'>
        logo
      </div>
      <div className='text-[18px]'>
        {league_name.name}
      </div>
    </div>
  )
  return (
    <div className=''>
      <DataList
        title='Leagues'
        data={leagues}
        card={Card}
      />  
      <AddLeagueButton/>
    </div>
  )
}

export default LeaguesButtons