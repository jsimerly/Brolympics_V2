import ManageEventWrapper from "./ManageEventWrapper"
import {useState, useEffect} from 'react'
import ScoringSettings from "./ScoringSettings"
import {fetchUpdateEvent} from '../../../../api/fetchEvents.js'


const ManageEvent_h2h = ({event}) => {
    const [formValues, setFormValues] = useState({});

    useEffect(() => {
        if (event) {
            setFormValues({...event});
        }
    }, [event]);
        
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            [name]: value
        }));
    };

    const handleUpdateClicked = () => {
        fetchUpdateEvent(formValues)
    }
 
  return (
    <ManageEventWrapper name={event.name}>
        <div className="flex flex-col">
            <h2 className="py-2">Match Settings</h2>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">Number of Matches</h3>
                    <p className="text-[10px]">The number of matches each team will compete in during group play.</p>
                </div>
                <input
                    value={formValues.n_matches || ''}
                    name='n_matches'
                    onChange={handleInputChange}
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                    type='number'
                />
            </div>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    <h3 className="font-semibold">Max Concurrent Matches</h3>
                    <p className="text-[10px]">The number of max possible simulatnious matches. <br/> Ex: 2 sets of cornhole boards. Leave blank for no max.</p>
                </div>
                <input 
                    value={formValues.n_active_limit || ''}
                    name='n_active_limit'
                    onChange={handleInputChange}
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center"
                    type='number'
                />
            </div>
            <div className="flex items-center justify-between min-h-[50px]">
                <div>
                    {/* Fake form input for now until I can create more options for brackets */}
                    <h3 className="font-semibold">Bracket Size</h3>
                    <p className="text-[10px]">The number of teams to make the playoffs.</p>
                </div>
                <div
                    className="p-1 border rounded-md border-primary h-[40px] w-[60px] bg-white text-center justify-center flex items-center"
                  
                > 4 </div>
            </div>
            <ScoringSettings
                formValues={formValues}
                setFormValues={setFormValues}
                handleInputChange={handleInputChange}
            />
            <button 
                className="w-full p-2 mt-3 font-semibold text-white rounded-md bg-primary"
                onClick={handleUpdateClicked}
            >
                Update {event.name}
            </button>
        </div>
    </ManageEventWrapper>

  )
}

export default ManageEvent_h2h