import Gold from '../../assets/svgs/gold.svg'
import Silver from '../../assets/svgs/silver.svg'
import Bronze from '../../assets/svgs/bronze.svg'


const BrolympicsCard_Upcoming = ({props}) => (
    <div className='p-3 border rounded-md border-primary'>
        <div className="flex items-center justify-between">
            <div className="flex gap-3 item-center">
                <div className='bg-white h-[40px] w-[40px] rounded-lg text-black'>
                    logo
                </div>
                <h3 className="text-[20px] font-bold flex items-center">{props.name}</h3>
            </div>
            <div className="text-[12px] flex items-end justify-end">
                {props.date}
            </div>
        </div>
        <div className="flex pt-3 text-[14px]">
            <div className="pr-2 text-[16px]">
                Events:
            </div>
            <div className="">
                {props.events.map((event, i) => (
                    i !== 0 ? `, ${event}` : event
                ))}
            </div>
        </div>
        <div className="flex pt-3 text-[14px]">
            <div className="pr-2 text-[16px]">
                Teams:
            </div>
            <div className="">
                {props.teams.map((team, i) => (
                    i !== 0 ? `, ${team}` : team
                ))}
            </div>
        </div>
    </div>
)

const BrolympicsCard_Completed = ({props}) => (
    <div className='p-3 border rounded-md border-primary'>
        <div className="flex items-center justify-between">
            <div className="flex gap-3 item-center">
                <div className='bg-white h-[40px] w-[40px] rounded-lg text-black'>
                    logo
                </div>
                <h3 className="text-[20px] font-bold flex items-center">{props.name}</h3>
            </div>
            <div className="text-[12px] flex items-end justify-end">
                {props.date}
            </div>
        </div>
        <div className='flex flex-col justify-center gap-3 px-2 pt-4'>
            <div className='flex gap-1'>
                <img src={Gold} className='h-[20px]'/>
                {props.winner}
            </div>
            <div className='flex gap-1'>
                <img src={Silver} className='h-[20px]'/>
                {props.second}
            </div>
            <div className='flex gap-1'>
                <img src={Bronze} className='h-[20px]'/>
                {props.third}
            </div>
        </div>
    </div>
)

const League = () => {
    const brolympics = [
        {
            'name':'Summer 2022',
            'is_complete': true,
            'winner' : 'Poland',
            'second' : 'Saint Vincent and the Grenadines',
            'third' : 'Third Dynasty of Ur',
            'date' : 'Aug 23 2022',
            'events': ['Cornhole', 'Bowling', 'Beer Pong', 'Trivia'],
            'teams' : ['El Salvador', 'United State', 'Saint Vincent and the Grenadines', 'Poland', 'France']
        },
        {
            'name':'Summer 2023',
            'is_complete': false,
            'winner' : '',
            'date' : 'Aug 19 2023',
            'events': ['Cornhole', 'Bowling', 'Beer Pong', 'Trivia', 'Foot Tag'],
            'teams' : ['El Salvador', 'United State of America', 'Saint Vincent and the Grenadines', 'Poland', 'France']
        },
    ]
  return (
    <div className='min-h-[calc(100vh-80px)] px-6 py-3 text-white bg-neutral'>
        <div>
            <h1 className='text-[26px] font-bold leading-none pt-3'>
                Stuck in Highschool
            </h1>
            <span className='text-[12px]'>Founded: 2014</span>
        </div>
        <div>
            <h2 className="py-3 ml-1 font-bold"> Upcoming Brolympics </h2>
            <div className="flex flex-col gap-3">
                {brolympics.map((brolympic, i) => {
                    if (!brolympic.is_complete){
                        return(
                            <BrolympicsCard_Upcoming props={brolympic} key={i}/>
                        )
                    }
                })}
            </div>
            <h2 className="py-3 ml-1 font-bold"> Finished Brolympics </h2>
            <div className="flex flex-col gap-3">
                {brolympics.map((brolympic, i) => {
                    if (brolympic.is_complete){
                        return(
                            <BrolympicsCard_Completed props={brolympic} key={i}/>
                        )
                    }
                })}
            </div>
        </div>



    </div>
  )
}

export default League