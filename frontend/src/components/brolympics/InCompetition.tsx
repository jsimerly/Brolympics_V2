import {useState} from 'react'
import InCompetitions_h2h from './inCompetitions/InCompetitions_h2h'
import InCompetition_ind from './inCompetitions/InCompetition_ind'
import InCompetition_team from './inCompetitions/InCompetition_team'


const InCompetition = ({activeComp}) => {

  const getCompComponent = (type, uuid) => {
    switch (type) {
      case 'h2h':
        return <InCompetitions_h2h/>
      case 'ind':
        return <InCompetition_ind />
      case 'team':
        return <InCompetition_team />
      default:
        return null
    }
  }

  return (
    <div className=''>
      {!activeComp.is_available &&
        getCompComponent(activeComp.type, activeComp.comp_uuid)
      }
    </div>
  )
}

export default InCompetition