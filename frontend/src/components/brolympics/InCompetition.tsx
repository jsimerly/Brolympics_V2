import {useState} from 'react'
import InCompetitions_h2h from './inCompetitions/InCompetitions_h2h'
import InCompetition_ind from './inCompetitions/InCompetition_ind'
import InCompetition_team from './inCompetitions/InCompetition_team'


const InCompetition = ({comp}) => {

  const getCompComponent = (type, props) => {
    switch (type) {
      case 'h2h':
        return <InCompetitions_h2h {...props}/>
      case 'ind':
        return <InCompetition_ind {...props}/>
      case 'team':
        return <InCompetition_team {...props}/>
      default:
        return null
    }
  }

  return (
    <div className=''>
      {comp &&
        getCompComponent(comp.type, comp)
      }
    </div>
  )
}

export default InCompetition