
import TeamsBlock from './TeamBlock';

const ActiveCompetition_h2h = ({name, team_1_name, team_1_record, team_1_img, team_2_name, team_2_record, team_2_img}) => {



  return (
    <div className='p-2'>
      <TeamsBlock
        name={name}
        team_1_name={team_1_name}
        team_1_record={team_1_record}
        team_1_img={team_1_img}
        team_2_name={team_2_name}
        team_2_record={team_2_record}
        team_2_img={team_2_img}
      />
    </div>
  )
}

export default ActiveCompetition_h2h