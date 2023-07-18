import React from 'react'

const TeamsBlock = ({name, team_1_name, team_1_record, team_1_img, team_2_name, team_2_record, team_2_img}) => {
    
    const TeamBlock = ({name, record, img, reverse=false}) => {
        let fontSize;
        if (name) {
          if (name.length <= 10) {
            fontSize = '16px';
          } else if (name.length <= 16) {
            fontSize = '14px';
          } else if (name.length <= 20) {
            fontSize = '12px';
          } else {
            fontSize = '10px'
          }
        }
        
        return (
          <div className=''>
            <div className={`flex ${reverse ? 'flex-row-reverse justify-start' : 'flex-row justify-start'} gap-2`}>
              <div className='h-[60px] w-[60px] min-w-[60px] bg-white rounded-md'>
                img
              </div>
              <div className={`flex flex-col justify-center items-${reverse ? 'end' : 'start'}`}>
                <div 
                  className={`flex font-bold items-center ${reverse ? 'justify-end text-end' : 'justify-start text-start'}`}
                  style={{ fontSize }}
                >
                    {name}
                </div>
                <div className='text-[12px]'>{record}</div>
              </div>
            </div>
        </div>
        );
      };
      
  return (
    <>
        <h2 className='pb-2 font-bold'>{name}</h2>
        <div className='flex'>
            <div className='w-1/2'>
            <TeamBlock name={team_1_name} record={team_1_record} img={team_1_img}/>
            </div>
            <div className='flex items-center px-3'>
                <div className='text-center rounded-full w-[28px] flex items-center justify-center'>vs</div>
            </div>
            <div className='w-1/2'>
            <TeamBlock name={team_2_name} record={team_2_record} img={team_2_img} reverse={true}/>
            </div>
        </div>
    </>
  )
}

export default TeamsBlock