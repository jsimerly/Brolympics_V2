import React from 'react'

export const TeamNode = ({name, seed, score, img}) => {
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

    return(
        <div 
            className={`p-1 border rounded-md border-primary h-[40px] flex gap-1 items-center justify-between w-[200px] min-w-[200px]`}
            style={{fontSize}}
        >
            <div className='flex items-center justify-start gap-1'>
                <div className='h-[30px] w-[30px] bg-white rounded-md'>l</div>
                <div>{seed}</div>
                <div>{name}</div>
            </div>
            <div className='text-[16px] px-1'>{score}</div>
        </div>
    )
}


const BracketNode = ({team_1_name, team_1_seed, team_1_score, team_1_img, team_2_name, team_2_seed, team_2_score, team_2_img}) => {
  return (
    <div className='flex gap-1'>
        <div className='flex flex-col gap-1'>
            <TeamNode
                name={'Third Dynasty of Ur'}
                seed={1}
                score={21}
            />
            <TeamNode
                name={'Greece'}
                seed={4}
                score={14}
            /> 
        </div>
        <div className='flex items-center pl-3'>
            <div className='h-[2px] bg-primary w-[16px]'/>
        </div>
    </div>
  )
}
export default  BracketNode