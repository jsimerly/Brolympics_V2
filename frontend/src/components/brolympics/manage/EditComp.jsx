import { useState } from "react"
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const H2hComp = ({team_1, team_1_score, team_2, team_2_score, uuid}) => {
  const handleUpdateClicked = async () => {
    
  }
  return(
    <div className='relative flex flex-col gap-1 p-2 border'>
      <div className='flex items-center'>
        <div>{team_1}:</div> <input value={team_1_score} className='p-2 rounded-md w-[60px] border ml-1'/>
      </div>
      <div className='flex items-center'>
      <div>{team_2}:</div> <input value={team_2_score} className='p-2 rounded-md w-[60px] border ml-1'/>
      </div>
      <button 
        className='absolute px-2 py-1 text-white rounded-md bottom-2 right-2 bg-primary'
        onClick={handleUpdateClicked}
      >
        Update
      </button>
    </div>
  )
}

const IndComp = ({team, player_1_name, player_1_score, player_2_name, player_2_score, uuid}) => {
  const handleUpdateClicked = async () => {
    
  }
  return(
    <div className='relative flex flex-col gap-1 p-2 border'>
      {team}
      <div className='flex items-center'>
        <div>{player_1_name}:</div> <input value={player_1_score} className='p-2 rounded-md w-[60px] border ml-1'/>
      </div>
      <div className='flex items-center'>
      <div>{player_2_name}:</div> <input value={player_2_score} className='p-2 rounded-md w-[60px] border ml-1'/>
      </div>
      <button 
        className='absolute px-2 py-1 text-white rounded-md bottom-2 right-2 bg-primary'
        onClick={handleUpdateClicked}
      >
        Update
      </button>
    </div>
  )
}


const TeamComp = ({team, team_score, uuid}) => {
  const handleUpdateClicked = async () => {
    
  }
  return(
    <div className="flex items-center justify-between p-2 border rounded-md">
      <div>
        {team}: <input value={team_score} className='p-2 rounded-md w-[60px] border ml-1'/>
      </div>
      <button 
        className='px-2 py-1 text-white rounded-md bottom-2 right-2 bg-primary'
        onClick={handleUpdateClicked}
      >
        Update
      </button>
    </div>
  )
}

const ClickCard = ({event, children}) => {
  const [isOpen, setIsOpen] = useState(false)
  const handleToggle = () => setIsOpen(isOpen => !isOpen)
  
  return (
    <div className="w-full py-3">
      <div onClick={handleToggle} className="flex justify-between pb-3">
        <h3 className="font-semibold text-[18px]">{event.name}</h3>
        {isOpen ? <ExpandLessIcon/> : <ExpandMoreIcon/>}
      </div>

      {isOpen && children}
    </div>
  );
};


const EditComp = () => {
  const h2h_events = [
    {name:'cornole',
    comps:[{team_1:'Greece', team_1_score: 21, team_2:"Germany", team_2_score:11},
    {team_1:'Poland', team_1_score: 17, team_2:"Greece", team_2_score:21},
    {team_1:'Germany', team_1_score: 14, team_2:"Poland", team_2_score:21},
    {team_1:'Greece', team_1_score: 21, team_2:"USA", team_2_score:11},]
    },
  ]
  const ind_events = [
    {name:'golf',
    comps:[
      {team:'Germany', player_1_score:21, player_1_name:'Jacob', player_2_score:14, player_2_name:'Timmy'
      },
      {team:'Greece', player_1_score:17, player_1_name:'Jim', player_2_score:21, player_2_name:'Jake'
      },
      {team:'GPoland', player_1_score:21, player_1_name:'Tanner', player_2_score:19, player_2_name:'Tim'
      },
    ]
  }

  ]
  const team_events = [
    {name:'Triva',
    comps:[
      {team:'Greece', team_score: 140},
      {team:'Germany', team_score: 140},
    ]}
  ]

  return (
    <div>
      <h2>Ind Events</h2>
      <ul>
        {ind_events.map((event, i) => (
          <div key={i + "_ind_event_edit"}>
            {i !== 0 && <div className="w-full" />}
            <ClickCard event={event}>
              <ul className="space-y-2">
                {event.comps.map((comp, i) => (
                  <IndComp {...comp} key={i + "_ind_edit_comp"} />
                ))}
              </ul>
            </ClickCard>
          </div>
        ))}
      </ul>
      <h2>Head to Head Events</h2>
      <ul>
        {h2h_events.map((event, i) => (
          <div key={i + "_ind_event_edit"}>
            {i !== 0 && <div className="w-full" />}
            <ClickCard event={event}>
              <ul className="space-y-2">
                {event.comps.map((comp, i) => (
                  <H2hComp {...comp} key={i + "_ind_edit_comp"} />
                ))}
              </ul>
            </ClickCard>
          </div>
        ))}
      </ul>
      <h2>Team Events</h2>
      <ul>
        {team_events.map((event, i) => (
          <div key={i + "_ind_event_edit"}>
            {i !== 0 && <div className="w-full" />}
            <ClickCard event={event}>
              <ul className="space-y-2">
                {event.comps.map((comp, i) => (
                  <TeamComp {...comp} key={i + "_ind_edit_comp"} />
                ))}
              </ul>
            </ClickCard>
          </div>
        ))}
      </ul>
    </div>
  );
};

export default EditComp;