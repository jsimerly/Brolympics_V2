import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {fetchTeamInvite, fetchJoinTeam} from '../../api/fetchInvites.js'
import InviteWrapper from "./InviteWrapper.js";


const TeamInvite = () => {


  return (
    <InviteWrapper
      fetchInfo={fetchTeamInvite}
      fetchJoin={fetchJoinTeam}
      joinText={'Join Brolympics'}
    >
      Team Invite Here
    </InviteWrapper>
  )
}

export default TeamInvite