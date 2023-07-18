import CurrentBrolympics from "./CurrentBrolympics"
import LeaguesButtons from "./LeaguesButtons"
import Options from "./Options"
import UpcomingBrolympics from "./UpcomingBrolympics"
import UpcomingCompetitions from "./UpcomingComps"

const Slideout = ({open}) => {
    const leagues = [
        {'name':'League 1'},
        {'name':'League 2'}
    ]
    const current_brolympics = []

    const upcoming_brolympics = [
        {
        'name': 'Summer 2023',
        'projected_start_date' : 'Aug 19',
        'projected_end_date' : 'Aug 20',
        }
    ]
    const upcoming_competitions = [
        {
            'name': 'Cornhole',
            'projected_date' : 'Aug 19 6:00 p.m.',
            'location' : 'Holland Park'
        },
    ]


  return (
    <>
        {open &&
            <div className="fixed top-[80px] left-0 w-full z-30">
                <div className='flex flex-col h-[calc(100vh-80px)] bg-neutral text-offWhite opacity-[98%] px-6 py-3 gap-3'>
                    <LeaguesButtons leagues={leagues}/>
                    <CurrentBrolympics current_brolympics={current_brolympics}/>
                    <UpcomingBrolympics upcoming_brolympics={upcoming_brolympics}/>
                    <UpcomingCompetitions upcoming_competitions={upcoming_competitions}/>

                    
                </div>
                <div>
                    <Options/>
                </div>
            </div>
        }
    </>
  )
}

export default Slideout