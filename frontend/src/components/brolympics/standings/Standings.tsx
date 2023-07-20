import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
import DiamondOutlinedIcon from '@mui/icons-material/DiamondOutlined';
import Gold from '../../../assets/svgs/gold.svg'
import Silver from '../../../assets/svgs/silver.svg'
import Bronze from '../../../assets/svgs/bronze.svg'

const Standings = () => {
  const standings = [
      {
        'name' : 'Poland',
        'rank' : 2,
        'points' : 15,
      },
      {
        'name' : 'Third Dynasty of Ur',
        'rank' : 1,
        'points' : 23,
      },
      {
        'name' : 'Greece',
        'rank' : 2,
        'points' : 15,
      },
      {
        'name' : 'Germany',
        'rank' : 4,
        'points' : 11,
      },    {
        'name' : 'El Salvador',
        'rank' : 5,
        'points' : 8,
      },
      {
        'name' : 'Norway',
        'rank' : 6,
        'points' : 6,
      },
      {
        'name' : 'North Korea',
        'rank' : 7,
        'points' : 4,
      },
      {
        'name' : 'Netherlands',
        'rank' : 7,
        'points' : 4,
      },
    ]

    const sortedStandings = [...standings].sort((a, b) => a.rank - b.rank);

    const podiumList = [
      {
        'name' : 'Cornhole',
        'winner' : 'Third Dynasty of Ur',
        'second' : 'Greece',
        'third' : 'Norway',
      },
      {
        'name' : 'Bowling',
        'winner' : 'El Salvador',
        'second' : 'Germany',
        'third' : 'Third Dynasty of Ur',
      },
      {
        'name' : 'Go Karting',
        'winner' : 'France',
        'second' : 'Norway',
        'third' : 'Greece',
      },
    ]

  
  return (
    <div className='px-6 py-3'>
      <div>
        <h2 className='text-[20px] font-bold pb-2'>Overall Standings</h2>
        <table className='w-full border border-neutralLight'>
          <thead>
            <tr className='border text-primary border-neutralLight'>
              <th className='border border-neutralLight w-[60px] p-2'><NumbersOutlinedIcon/></th>
              <th className='pl-6 border border-neutralLight text-start text-[20px]'>Team</th>
              <th className='border border-neutralLight w-[80px]'><DiamondOutlinedIcon/>
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedStandings.map((team, i) => (
              <tr key={i+'_row'}>
                <td className='p-2 font-bold text-center text-[18px] border-r border-neutralLight'>{team.rank}</td>
                <td className='pl-6 text-start text-[20px] border-r border-neutralLight'>{team.name}</td>
                <td className='p-2 text-center border-r text-[18px] border-neutralLight'>{team.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className='py-6'>
        <h2 className='text-[20px] font-bold pb-2'>Event Podiums</h2>
        {podiumList.length === 0 && 'No events have been completed yet.'}
        <ul className='flex flex-col gap-6'>
        {podiumList.map((event, i) => (
          <div key={i+"_podium"}>
            <h3 className='font-bold'>{event.name}</h3>
            <div className='flex flex-col justify-center gap-2 px-2 pt-2'>
                <div className='flex gap-2'>
                    <img src={Gold} className='h-[20px]'/>
                    {event.winner}
                </div>
                <div className='flex gap-2'>
                    <img src={Silver} className='h-[20px]'/>
                    {event.second}
                </div>
                <div className='flex gap-2'>
                    <img src={Bronze} className='h-[20px]'/>
                    {event.third}
                </div>
              </div>
          </div>
        ))}
        </ul>
      </div>
  </div>
  )
}

export default Standings