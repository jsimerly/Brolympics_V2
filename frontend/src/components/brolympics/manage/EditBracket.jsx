import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useEffect, useState } from 'react';
import { fetchBracketData } from '../../../api/activeBro/fetchAdmin';
import { useParams } from 'react-router-dom';

const ClickCard = ({event, children}) => {
  const [isOpen, setIsOpen] = useState(false)
  const handleToggle = () => setIsOpen(isOpen => !isOpen)
  

  return (
    <div className="w-full py-3">
      <div onClick={handleToggle} className="flex justify-between pb-3">
        <h3 className="font-semibold text-[18px]">{event.name}</h3>
        {isOpen ? <ExpandLessIcon/> : <ExpandMoreIcon/>}
      </div>

      {isOpen && children}
    </div>
  )
}

const EditBracket = () => {
  const {uuid} = useParams()
  const [events, setEvents] = useState([])

  useEffect(()=>{
    const getEvents = async () => {
      const response = await fetchBracketData(uuid)
      if (response.ok){
        const data = await response.json()
        console.log(data)
      } else {
        console.log('error for now')
      }
    }
    getEvents()
  },[])

  return (
    <div>EditBracket</div>
  )
}

export default EditBracket