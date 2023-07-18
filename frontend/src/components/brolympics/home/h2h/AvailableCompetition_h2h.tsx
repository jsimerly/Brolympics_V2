import TeamsBlock from "./TeamBlock"

const AvailableCompetition_h2h = ({name, team_name, team_record, team_img, opponent_name, opponent_record, opponent_img}) => {



  return (
    <div className='p-2 border border-gray-200 rounded-md bg-neutralLight'>
      <TeamsBlock
        name={name}
        team_1_name={team_name}
        team_1_record={team_record}
        team_1_img={team_img}
        team_2_name={opponent_name}
        team_2_record={opponent_record}
        team_2_img={opponent_img}
      />
      <div className="flex items-center justify-center w-full pt-6">
        <button className='w-1/2 p-2 font-bold rounded-md bg-primary'>
          Start
        </button>
      </div>
    </div>
  )
}

export default AvailableCompetition_h2h