import EventWrapper from './EventWrapper';

const Matchup = ({team_1_name, team_1_score, team_2_name, team_2_score, result, is_active}) => {

    let borderColor;
    switch (result) {
        case 'won':
            borderColor = 'border-primary';
            break;
        case 'lost':
            borderColor = 'border-errorRed';
            break;
        default:
            borderColor = 'border-gray-200';
    }
    
    return (
    <div 
        className={`flex items-center justify-center p-1 border rounded-md 
        bg-neutral ${borderColor}
        ${is_active && 'border-[2px]'}
        `}
    >
        <div className='flex items-center justify-center w-full'>
            <div className='w-2/5'> {team_1_name}</div>
            <div className='w-1/5 text-center'>{team_1_score} : {team_2_score}</div>
            <div className='w-2/5'> {team_2_name}</div> 
        </div>

    </div>
    )
}
    

const EventDropdown_H2h = ({decimal_places, score_for, score_against, sos_wins, sos_losses, comps, is_active}) => (
    <div className={`py-2 border-t ${is_active ? 'border-neutral' : 'border-neutralLight'} `}>
        <div className='flex justify-between'>
            <div className='w-1/2'>
                <h3 className='font-bold'>Margin</h3>
                <div className='grid grid-cols-2'>
                    <div>Pts For</div><div>{score_for} pts</div>
                    <div>Pts Against</div><div>{score_against} pts</div>
                </div>
            </div>
            <div className='w-1/2'>
                <h3 className='font-bold'>Strengh of Schedule</h3>
                <div className='grid grid-cols-2'>
                    <div>Wins</div><div>{sos_wins} </div>
                    <div>Losses</div><div>{sos_losses} </div>
                </div>
            </div>
        </div>
        <h4 className='pt-2 font-bold'>Competitions</h4>    
        <div className='flex flex-col gap-1 py-1'>
            {comps.map((comp, i) => (
                <Matchup {...comp}/>
            ))}
            {comps.length === 0 && 'Event has not started yet.'}
        </div>
    </div>
)


const Event_h2h = ({name, decimal_places, wins, losses, ties, score_for, score_against, sos_losses, sos_wins, rank, points, is_final, is_active, comps}) => {

    return (
        <EventWrapper
            name={name}
            rank={rank}
            points={points}
            display_score={wins+'-'+losses}
            is_active={is_active}
            is_final={is_final}
        >
            <EventDropdown_H2h 
                decimal_places={decimal_places}
                score_for={score_for}
                score_against={score_against}
                sos_wins={sos_wins}
                sos_losses={sos_losses}
                comps={comps}
                is_active={is_active}
            />
        </EventWrapper>
    )
}

export default Event_h2h