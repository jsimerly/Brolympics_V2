import HomeActive from './HomeActive'
import HomeAdmin from './HomeAdmin'
import HomePost from './HomePost'
import HomePre from './HomePre'

import { useState, useEffect } from 'react'


const Home = ({brolympics, status}) => {
  const componentMap = {
    'active': HomeActive,
    'pre_admin': HomeAdmin,
    'pre': HomePre,
    'post': HomePost,
  }

  const Component = componentMap[status] || HomeActive
    
  return (
    <div>
        <Component {...brolympics}/>
    </div>
  )
}

export default Home