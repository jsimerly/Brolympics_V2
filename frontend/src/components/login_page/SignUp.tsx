import {useState} from 'react'
import { useSwipeable } from 'react-swipeable';
import CreateAccount from './CreateAccount';
import LogIn from './LogIn';

const SignUp = () => {
    const [currentPage, setCurrentPage] = useState('createAccount')

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
    <div className='flex flex-col h-[calc(100vh-80px)] border p-3' {...swipeHandlers}>
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
      <div className='flex flex-1 h-full mx-3 border'>
        Image Here
      </div>

      {currentPage === 'createAccount' ? (
        <CreateAccount/>
      ) : (
        <LogIn/>
      )}
    </div>
  );
};

export default SignUp;