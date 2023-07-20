import TeamsDropdown from "./TeamsDropdown";
import Podium from '../../../assets/svgs/podium.svg'
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
import DiamondOutlinedIcon from '@mui/icons-material/DiamondOutlined';
import EmojiEventsOutlinedIcon from '@mui/icons-material/EmojiEventsOutlined';

import Event_h2h from "./events/Event_h2h";
import Event_ind from "./events/Event_ind";
import Event_team from "./events/Event_team";

const Team = () => {
  const teams = [
    'Dynasty of Ur',
    'El Salvador',
    'Poland',
    'France',
    'Greece',
    'Norway',
    'North Korea',
  ]

  const team_info = {
    'player_1' : 'Jacob Simerly',
    'player_2' : 'Frank Sergi',
    'rank' : 1,
    'points' : 23,
    'total_wins' : 1,
    'total_podiums' : 1,
  }
  
  const eventRanking = [
    {
      'name' : 'Cornhole',
      'type' : 'h2h',
      'decimal_places' : 0,
      'wins' : 4,
      'losses' : 0,
      'ties' : 0,
      'score_for' : 84,
      'score_against' : 22,
      'sos_wins' : 4,
      'sos_losses' : 7,
      'sos_ties' : 0,
      'rank' : 1,
      'points' : 12,
      'is_final' : true,
      'is_active' : false,
      'comps' : [
        {
          'winner' : 'Third Dynasty of Ur',
          'team_1_name' : 'Third Dynasty of Ur',
          'team_1_score' : 21,
          'team_2_name' : 'Poland',
          'team_2_score' : 8,
          'is_active': false,
        },
        {
          'winner' : 'Third Dynasty of Ur',
          'team_1_name' : 'Third Dynasty of Ur',
          'team_1_score' : 21,
          'team_2_name' : 'France',
          'team_2_score' : 3,
          'is_active' : false,
        },
        {
          'winner' : 'Third Dynasty of Ur',
          'team_1_name' : 'Greece',
          'team_1_score' : 5,
          'team_2_name' : 'Third Dynasty of Ur',
          'team_2_score' : 21,
          'is_active' : false,
        },
        {
          'winner' : 'Germany',
          'team_1_name' : 'Third Dynasty of Ur',
          'team_1_score' : 21,
          'team_2_name' : 'Germany',
          'team_2_score' : 6,
          'is_active' : false,
        },
      ]
    },
    {
      'name' : 'Go Karting',
      'type' : 'ind',
      'decimal_places' : 3,
      'score' : 24.623,
      'rank' : 3,
      'points' : 9,
      'is_final' : true,
      'is_active' : false,
      'comps' : [
        {
        'player_1_name' : 'J. Simerly',
        'player_1_score' : 24.324,
        'player_2_name' : 'F. Sergi',
        'player_2_score' : 24.873,
        'team_score' : 24.623,
        'is_active' : false,
        },
      ]
    },
    {
      'name' : 'Beer Pong',
      'type' : 'h2h',
      'decimal_places' : 0,
      'wins' : 1,
      'losses' : 1,
      'ties' : 0,
      'score_for' : 23,
      'score_against' : 20,
      'sos_wins' : 7,
      'sos_losses' : 2,
      'sos_ties' : 0,
      'rank' : 6,
      'points' : 3.5,
      'is_active' : true,
      'is_final' : false,
      'comps' : [
        {
          'winner' : 'Third Dynasty of Ur',
          'team_1_name' : 'Third Dynasty of Ur',
          'team_1_score' : 21,
          'team_2_name' : 'Poland',
          'team_2_score' : 8,
          'is_active': false,
        },
        {
          'winner' : 'France',
          'team_1_name' : 'Third Dynasty of Ur',
          'team_1_score' : 21,
          'team_2_name' : 'France',
          'team_2_score' : 3,
          'is_active' : false,
        },
        {
          'winner' : null,
          'team_1_name' : 'Greece',
          'team_1_score' : 0,
          'team_2_name' : 'Third Dynasty of Ur',
          'team_2_score' : 0,
          'is_active' : true,
        },        
        {
          'winner' : null,
          'team_1_name' : 'Germany',
          'team_1_score' : 0,
          'team_2_name' : 'Third Dynasty of Ur',
          'team_2_score' : 0,
          'is_active' : false,
        },
      ]
    },    
    {
      'name' : 'Bowling',
      'type' : 'ind',
      'decimal_places' : 0,
      'score' : 0,
      'rank' : 1,
      'points' : 6,
      'is_active' : false,
      'is_final' : false,
      'comps' : []
    },
  ]

  const TeamInfo = ({player_1, player_2, rank, points, total_wins, total_podiums}) => (
    <div className="flex items-center justify-center w-full gap-3 px-6">
      <div className="flex flex-col items-center justify-center w-full p-3 border rounded-md border-primary">
        <div className="flex justify-around w-3/4 py-3 pb-6">
          <span className="font-bold text-[18px]">{player_1}</span><span className="font-bold text-[18px]">{player_2}</span>
        </div>
        <div className="flex justify-center w-full gap-6">
          <div className="flex">
            <NumbersOutlinedIcon className="text-primary"/>
            <span className="text-[16px] font-bold pl-3">
              {rank}st   
            </span>
          </div>
          <div className="flex">
            <DiamondOutlinedIcon className="text-primary"/>
            <span className="text-[16px] font-bold pl-3">
              {points} pts   
            </span>
          </div>
          <div className="flex">
            <EmojiEventsOutlinedIcon className="text-primary"/>
            <span className="text-[16px] font-bold pl-3">
              {total_wins}
            </span>
          </div>
          <div className="flex">
            <img src={Podium} className="text-white h-[30px] w-[40px]"/>
            <span className="text-[16px] font-bold pl-3">
              {total_podiums}
            </span>
          </div>
        </div>
      </div>
    </div>
  )

  const getEventComponent = (type, props) => {
    switch (type) {
      case 'h2h':
        return <Event_h2h {...props} team='Third Dynasty of Ur'/>
      case 'ind':
        return <Event_ind {...props} team='Third Dynasty of Ur'/>
      case 'team':
        return <Event_team {...props} team='Third Dynasty of Ur'/>
    }
  }
  
  return (
    <div className='w-full'>
      <TeamsDropdown teams={teams}/>
      <TeamInfo {...team_info}/>
      
      <div className="py-3">
        <h2 className="text-[20px] font-bold px-6">Events</h2>
        {eventRanking.map((event, i) => 
          <div key={i+"_teams"}>
            {getEventComponent(event.type, event)}
            {i !== eventRanking.length - 1  && 
            <div className="w-full px-6">
              <div className="w-full h-[1px] bg-neutralLight" />
            </div>
            }
          </div>

        )}
      </div>

    </div>
  );
}

export default Team