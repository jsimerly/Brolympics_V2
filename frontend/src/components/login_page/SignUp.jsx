import {useState} from 'react'
import { useSwipeable } from 'react-swipeable';
import CreateAccount from './CreateAccount';
import LogIn from './LogIn';

const SignUp = ({endPath='/'}) => {
    const [currentPage, setCurrentPage] = useState('createAccount')
    
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');

    const userState = { 
        firstName, setFirstName, 
        lastName, setLastName, 
        email, setEmail, 
        password, setPassword, 
        phoneNumber, setPhoneNumber 
    };
      

    const handlePageChange = (page) => {
        setCurrentPage(page)
    }

    const swipeHandlers = useSwipeable({
        onSwipedLeft: () => handlePageChange('signIn'),
        onSwipedRight: () => handlePageChange('createAccount'),
        preventDefaultTouchmoveEvent: true,
        trackMouse: true,
      });

  return (
    <div className='flex flex-col h-[calc(100vh-60px)] py-3 overflow-hidden' {...swipeHandlers}>
      <div className='flex items-center justify-center w-full gap-6 p-3'>
        <button
          className={`w-1/2 text-end ${currentPage === 'createAccount' ? 'font-bold' : ''}`}
          onClick={() => handlePageChange('createAccount')}
        >
          Create Account
        </button>
        |
        <button
          className={`w-1/2 text-start ${currentPage === 'signIn' ? 'font-bold' : ''}`}
          onClick={() => handlePageChange('signIn')}
        >
          Sign-In
        </button>
      </div>
      <div className={`transition ease-in-out duration-200 flex relative
      ${currentPage === 'createAccount' ? 'translate-x-0' : 'transform -translate-x-full'}`}>
            <CreateAccount {...userState} endPath={endPath}/>
            <LogIn {...userState} endPath={endPath}/> 
      </div>
    </div>
  );
};

export default SignUp;