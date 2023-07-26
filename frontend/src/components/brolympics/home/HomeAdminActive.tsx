import {fetchEventsUnstarted} from '../../../api/activeBro/fetchAdmin.js'
import {useState, useEffect} from 'react'
import { useNavigate, useLocation, useParams } from 'react-router-dom'


const UnstartedEventCard = ({name, projected_start_date}) => {
    return (
        <div className='flex items-center justify-between p-3 border rounded-md border-primary'>
            <div>
                <h2 className='font-semibold'>
                    {name}
                </h2>

                {projected_start_date}
            </div>
            <button className='min-w-[100px] rounded-md bg-primary py-1'>
                Start
            </button>
        </div>
    )
}

const HomeAdminActive = () => {
    const {pathname} = useLocation()
    const uuid = pathname.split("/")[2];

    const [unstartedEvents, setUnstartedEvents] = useState([])
    useEffect(()=> {
        const getUnstartedEvents = async () => {
            const response = await fetchEventsUnstarted(uuid)
            if (response.ok){
                const data = await response.json()
                console.log(data)
                setUnstartedEvents(data)
            }
        }
        getUnstartedEvents()
    },[])

  return (
    <div>
        <div className='space-y-3'>
            {unstartedEvents.map((event, i) => (
                <UnstartedEventCard {...event}/>
            ))}
        </div>
    </div>
  )
}

export default HomeAdminActive
