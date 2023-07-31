import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const InviteWrapper = ({fetchInfo, fetchJoin, joinText, children,}) => {
    const {uuid} = useParams()
    const [info, setInfo] = useState()
    
    useEffect(() => {
      const getinfo = async () => {
        const response = await fetchInfo(uuid)

        if (response.ok) {
          const data = await response.json()
          console.log(data)
          setInfo(data)
        } else {
          const data = await response.json()
          console.log(data)
        }
      }
      getinfo()
    },[uuid])

    const joinClick = async () => {
      const response = await fetchJoin(uuid)

      if (response.ok){
        //navigate to the new league once we have those routes
      } else {
        //kick back an error
      }
    }

  return (
    <div className="flex flex-col items-center justify-between w-full h-[calc(100vh-80px)] p-6">
        {info &&
          React.cloneElement(children, { info })
        }
        <button 
              className="w-full p-3 font-bold text-white rounded-md bg-primary"
              onClick={joinClick}
            >
              {joinText}
        </button>

    </div>
  )
}

export default InviteWrapper