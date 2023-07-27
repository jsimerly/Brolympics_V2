import TeamsBlock from "./TeamBlock"
import {fetchStartComp} from "../../../../api/activeBro/fetchHome"

const AvailableCompetition_h2h = ({event, team_1, team_2, uuid, type}) => {
  const createRecordString = (team) => {
      const wins = team.wins
      const losses = team.losses
      const ties = team.ties

      return `${wins}-${losses}` + (ties ? `-${ties}` : '');
  }
  const onStartClicked = () => {
    fetchStartComp(uuid, type)
  }

  return (
    <div className='pb-3'>
      <TeamsBlock
        name={event}
        team_1_name={team_1.name}
        team_1_record={createRecordString(team_1)}
        team_1_img={team_1.img}
        team_2_name={team_2.name}
        team_2_record={createRecordString(team_2)}
        team_2_img={team_2.img}
      />
      <div className="flex items-center justify-center w-full pt-6">
        <button 
          className='w-1/2 p-2 font-bold rounded-md bg-primary'
          onClick={onStartClicked}
        >
          Start
        </button>
      </div>
    </div>
  )
}

export default AvailableCompetition_h2h