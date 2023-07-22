import { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext'

import { useState } from "react"
import { PasswordInput, PhoneNumberInput } from "../Util/Inputs"
import AccountValidator from '../Util/input_validation.js';
import ErrorMessages from "./ErrorMessages.js";


const LogIn = ({password, setPassword, phoneNumber, setPhoneNumber}) => {
    const {login} = useContext(AuthContext)

    const [passwordError, setPasswordError] = useState(false);
    const [phoneNumberError, setPhoneNumberError] = useState(false);

    const [errorMessages, setErrorMessages] = useState([])


    const handlePhoneNumberChange = (e) => setPhoneNumber(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);


    const validator = new AccountValidator()    

    const handleSignIn = async () => {
        validator.resetErrors()

        validator.validatePassword(password, setPasswordError)
        validator.validatePhoneNumber(phoneNumber, setPhoneNumberError)

        setErrorMessages(AccountValidator.errors)
        
        if (validator.errors.lenght > 0){
            return
        }
        login(phoneNumber, password)
    }
    
  return (
        <div className="flex flex-col items-center justify-end h-[calc(100vh-160px)] px-6 absolute translate-x-[100%] w-full">
            <div className="flex flex-1 w-full border">
                Image Here
            </div>
            <h2 className="text-[20px] font-bold">Sign-In</h2>
            <div className="flex flex-col w-full gap-4 py-4">
                <div className="w-full">
                    <PhoneNumberInput 
                        value={phoneNumber}
                        onChange={handlePhoneNumberChange}
                        error={phoneNumberError}
                    />
                </div>
                <div className="relative">
                    <PasswordInput
                        value={password}
                        onChange={handlePasswordChange}
                        error={passwordError}
                    />
                </div>
            </div>
            <ErrorMessages errorMessages={errorMessages}/>
            <button className="w-full p-3 font-bold text-white rounded-md bg-primary">
                Login
            </button>
            <div>
                <p className="underline text-[12px] pt-5 pb-7">I've Forgotten My Password</p>
            </div>
        </div>
  )
}

export default LogIn