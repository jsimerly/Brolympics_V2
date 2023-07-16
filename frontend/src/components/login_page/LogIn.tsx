import { useState } from "react"
import { PasswordInput } from "../Util/Inputs"
import AccountValidator from '../Util/input_validation.js';
import ErrorMessages from "./ErrorMessages.js";

const LogIn = ({email, setEmail, password, setPassword, phoneNumber, setPhoneNumber}) => {

    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const [phoneNumberError, setPhoneNumberError] = useState(false);

    const [errorMessages, setErrorMessages] = useState([])


    const handleEmailChange = (e) => setEmail(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);


    const validator = new AccountValidator()    

    const handleSignIn = async () => {
        validator.resetErrors()

        validator.validateEmail(email, setEmailError)
        validator.validatePassword(password, setPasswordError)
        validator.validatePhoneNumber(phoneNumber, setPhoneNumberError)

        setErrorMessages(AccountValidator.errors)
        
        if (validator.errors.lenght > 0){
            return
        }
    }
    
  return (
        <div className="flex flex-col items-center justify-end h-[calc(100vh-160px)] px-6 absolute translate-x-[100%] w-full">
            <div className="flex flex-1 w-full border">
                Image Here
            </div>
            <h2 className="text-[20px] font-bold">Sign-In</h2>
            <div className="flex flex-col w-full gap-4 py-4">
                <input 
                    className={`border border-neutral rounded-md pl-2 outline-neutral p-2 w-full ${emailError ? 'border-errorRed' : null}`}
                    placeholder="Phone or Email"
                    value={email}
                    onChange={handleEmailChange}
                />
                <div className="relative">
                    <PasswordInput
                        value={password}
                        onChange={handlePasswordChange}
                        error={passwordError}
                    />
                </div>
            </div>
            <ErrorMessages errorMessages={errorMessages}/>
            <button className="w-full p-3 rounded-md bg-primary">
                Create
            </button>
            <div>
                <p className="underline text-[12px] pt-5 pb-7">I've Forgotten My Password</p>
            </div>
        </div>
  )
}

export default LogIn