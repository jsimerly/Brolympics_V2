import React from 'react'
import AvailableCompetition_h2h from './h2h/AvailableCompetition_h2h';
import ActiveCompetition_h2h from './h2h/ActiveCompetition_h2h';
import AvailableCompetition_ind from './ind/AvailableCompetition_ind';
import ActiveCompetition_ind from './ind/ActiveCompetition_ind';
import AvailableCompetition_team from './team/AvailableCompetition_team';
import ActiveCompetition_team from './team/ActiveCompetition_team';

const CurrentEventCard = ({name, complete_perc}) => (
    <div className='pb-1 rounded-md '>
        <h3 className='pb-2'>
            {name}
        </h3>
        <div className='relative h-[2px] w-full bg-gray-200 rounded-full '>
            <div 
                className='absolute top-0 left-0 w-full h-full duration-200 ease-in-out rounded-full transition-width bg-primary'
                style={{width: `${complete_perc}%`}}
            />
        </div>
    </div>
)

const getAvailableComponent = (type, props) => {
    switch (type) {
        case 'h2h':
          return <AvailableCompetition_h2h {...props} />;
        case 'ind':
          return <AvailableCompetition_ind {...props} />;
        case 'team':
          return <AvailableCompetition_team {...props} />;
        default:
          return null;
      }
}

const getActiveComponent = (type, props) => {
    switch (type) {
        case 'h2h':
          return <ActiveCompetition_h2h {...props} />;
        case 'ind':
          return <ActiveCompetition_ind {...props} />;
        case 'team':
          return <ActiveCompetition_team {...props} />;
        default:
          return null;
      }
}

const EventBlock = ({ title, items, component: Component , component_func}) => {
    return (
        <div>
            <h2 className='text-[20px] font-bold pb-2'>{title}{items.length > 1 && 's'}</h2>
            { items.length === 0 ?
                `No ${title}`
                :
                <ul className='flex flex-col gap-2'>
                    {
                        items.map((item, i) => {
                            return (
                                <div key={i}>

                                    {component_func === null ? 
                                        <Component {...item} /> 
                                        : 
                                        <div>
                                        {i !==0 && <div className="w-full h-[1px] bg-neutralLight my-2"/>}
                                        {React.cloneElement(component_func(item.type, item), { key: i })}
                                        </div>
                                    }
                                     {/* Add divider here except for the last item */}
                                </div>
                            );
                        })
                    }
                </ul>
            }
        </div>
    );
}


const OutOfCompetitions = () => {
    const active_events = [
        {'name' : 'Cornhole', 'complete_perc' : 20},
        {'name' : 'Beer Pong', 'complete_perc' : 90},
        {'name' : 'Home Run Derby' , 'complete_perc' : 40}
    ]

    const available_competitions = [
        {
            'name' : 'Cornhole',
            'type' : 'h2h',
            'team_name' : 'Third Dynasty of Ur',
            'team_record' : '2-0',
            'team_img' : '',
            'opponent_name' : 'Poland',
            'opponent_record' : '0-1',
            'opponent_image' : ''
        },
        {
            'name' : 'Home Run Derby',
            'type' : 'ind',
            'team_name' : 'Third Dynasty of Ur',
            'team_img' : ''
         }
    ]
    
    const active_competitions = [
        {
            'name' : 'Beer Pong',
            'type' : 'h2h',
            'team_1_name' : 'El Salvador',
            'team_1_record' : '1-2',
            'team_2_name' : 'France',
            'team_2_record' : '1-0',
        },
        {
            'name' : 'Cornhole',
            'type' : 'h2h',
            'team_1_name' : 'USA',
            'team_1_record' : '1-2',
            'team_2_name' : 'St. Vincent and the Grenadines',
            'team_2_record' : '1-0',
        },        
        {
            'name' : 'Home Run Derby',
            'type' : 'ind',
            'team_name' : 'USA',
        },
    ]

    
  return (
    <div className='px-6 py-3'>
        <div className='flex flex-col gap-3'>
            <EventBlock 
                title="Current Event"
                items={active_events} 
                component={CurrentEventCard} 
                component_func={null}
            />
            <EventBlock 
                title="Available Competition" 
                items={available_competitions} 
                component={AvailableCompetition_h2h}
                component_func={getAvailableComponent}
            />
            <EventBlock 
                title="Active Competition" 
                items={active_competitions} 
                component={ActiveCompetition_h2h} 
                component_func={getActiveComponent}
            />
        </div>
    </div>
  )
}

export default OutOfCompetitions