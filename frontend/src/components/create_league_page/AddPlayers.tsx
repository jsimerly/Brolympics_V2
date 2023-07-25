import { useState } from 'react';
import CreateWrapper from './CreateWrapper'
import { PhoneNumberInput, PasswordInput } from "../Util/Inputs"
import AccountValidator from '../Util/input_validation.js';
import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import ContentCopyOutlinedIcon from '@mui/icons-material/ContentCopyOutlined';

const PhoneList = ({ label, values, setValues }) => (
  <div>
    <h4 className='pb-1 font-bold'>Add Players by {label}</h4>
    <div className='flex flex-col gap-2'>
      {values.map((value, i) => (
        <PhoneNumberInput 
            key={i}
            type="text"
            value={value}
            onChange={e => {
              const newValues = [...values];
              newValues[i] = e.target.value;
              setValues(newValues);
            }}
        />
      ))}
    </div>

    <button
      onClick={() => setValues([...values, ""])}
      className='py-3'
    >
      <AddCircleOutlineOutlinedIcon/> {label}
    </button>
  </div>
);

const InputList = ({ label, values, setValues }) => (
  <div>
    <h4 className='pb-1 font-bold'>Add Players by {label}</h4>
    <div className='flex flex-col gap-2'>
      {values.map((value, i) => (
        <input
          key={i}
          type="text"
          value={value}
          onChange={e => {
            const newValues = [...values];
            newValues[i] = e.target.value;
            setValues(newValues);
          }}
          className='w-full p-2 pl-2 border border-gray-200 rounded-md outline-neutral '
        />
      ))}
    </div>

    <button
      onClick={() => setValues([...values, ""])}
      className='py-3'
    >
      <AddCircleOutlineOutlinedIcon/> {label}
    </button>
  </div>
);
const AddPlayers = ({ step, nextStep }) => {
  const [phoneNumbers, setPhoneNumbers] = useState([""]);
  const [emails, setEmails] = useState([""]);

  const handleCreateClicked = () => {
    console.log('CREATE Event');
    console.log('Phone Numbers:', phoneNumbers);
    console.log('Emails:', emails);
    nextStep();
  }

  const [copySuccess, setCopySuccess] = useState(false);

  const copyToClipboard = async (text) => {
    if (!navigator.clipboard) {
      // Clipboard API not available
      return;
    }
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(true);
      setTimeout(() => {
        setCopySuccess(false);
      }, 3000);
    } catch (err) {
      console.log('Could not copy.')
    }
  }

  return (
    <CreateWrapper
      button_text={'Complete Set Up'}
      step={step}
      submit={handleCreateClicked}
      title={'Add Players to Your Brolympics'}
      description={'Share a link with your friends and fellow competitors'}
    >
      <PhoneList
        label="Phone"
        values={phoneNumbers}
        setValues={setPhoneNumbers}
      />
      
      <InputList
        label="Email"
        values={emails}
        setValues={setEmails}
      />

      <h4 className='pb-1 font-bold'>Copy the Link and Share with Friends</h4>
      <div 
        className='flex justify-between p-2 bg-white border rounded-md'
        onClick={()=>copyToClipboard('https://sleeper.com/i/k7N5Yxx00Ywz')}
      >
        https://sleeper.com/i/k7N5Yxx00Ywz
        <ContentCopyOutlinedIcon className='text-primary'/>
      </div>
      {copySuccess && <div className='text-primary'>Copied!</div>}
      
    </CreateWrapper>
  )
}

export default AddPlayers;
