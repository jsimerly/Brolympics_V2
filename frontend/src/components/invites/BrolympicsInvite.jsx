import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {fetchBrolympicsInvite, fetchJoinBrolympics} from '../../api/fetchInvites.js'
import InviteWrapper from "./InviteWrapper.jsx";


const BrolympicsInvite = () => {


  return (
    <InviteWrapper
      fetchInfo={fetchBrolympicsInvite}
      fetchJoin={fetchJoinBrolympics}
      joinText={'Join Brolympics'}
    >
      Brolympics Card Here
    </InviteWrapper>
  )
}

export default BrolympicsInvite