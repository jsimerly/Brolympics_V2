import { useContext, useState } from "react"
import { AuthContext } from '../../context/AuthContext'
import { useNavigate } from "react-router-dom";
import createImg from '../../assets/imgs/create_account_img_2.webp'

import { PhoneNumberInput, PasswordInput } from "../Util/Inputs"
import AccountValidator from '../Util/input_validation.js';
import ErrorMessages from "./ErrorMessages.jsx";

const CreateAccount = ({firstName, setFirstName, lastName, setLastName, password, setPassword, phoneNumber, setPhoneNumber, endPath}) => {
    const {createUser} = useContext(AuthContext)

    const [firstNameError, setFirstNameError] = useState(false);
    const [lastNameError, setLastNameError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const [phoneNumberError, setPhoneNumberError] = useState(false);
    const [errorMessages, setErrorMessages] = useState([])

    const handleFirstNameChange = (e) => setFirstName(e.target.value);
    const handleLastNameChange = (e) => setLastName(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);
    const handlePhoneNumberChange = (e) => setPhoneNumber(e.target.value);

    const navigate = useNavigate()
    const validator = new AccountValidator() 
    
    const handleCreateAccount = async () => {
        validator.resetErrors()

        validator.validateFirstName(firstName, setFirstNameError)
        validator.validateLastName(lastName, setLastNameError)
        validator.validatePassword(password, setPasswordError)
        validator.validatePhoneNumber(phoneNumber, setPhoneNumberError)

        setErrorMessages(AccountValidator.errors)
        
        if (validator.errors.lenght > 0){
            return
        }
        
        //navigate('verify')
        const cleanedPhoneNumber = validator.cleanPhoneNumber(phoneNumber)
        const response = await createUser(cleanedPhoneNumber, firstName, lastName, password)

        if (response.ok){
            navigate('verify', { state: { 
                phoneNumber: cleanedPhoneNumber,  
                firstName: firstName,
                lastName: lastName,
                password: password, 
                endPath: endPath,
            }});
        } else{
            const data = await response.json()
            console.log(data)
        }
    }
    
  return (
        <div className="flex flex-col items-center justify-end min-h-[calc(100vh-160px)] px-6 w-screen absolute">
            <div className="flex flex-1 w-full">
                <img src={createImg} className="object-fill w-full h-full"/>
            </div>
            <h2 className="text-[20px] font-bold">Create Your Account</h2>
            <div className="flex flex-col items-center justify-center gap-4 py-4">
                <div className="flex flex-row justify-between w-full gap-2">
                    <input
                        className={`w-1/2 border border-gray-200 rounded-md pl-2 outline-neutral p-2 ${firstNameError? 'border-errorRed' : null}`}
                        placeholder="First Name"
                        value={firstName}
                        onChange={handleFirstNameChange}
                    />
                    <input 
                        className={`w-1/2 border border-gray-200 rounded-md pl-2 outline-neutral p-2 ${lastNameError ? 'border-errorRed' : null}`}
                        placeholder='Last Name'
                        value={lastName}
                        onChange={handleLastNameChange}
                    />
                </div>
                <div className="flex flex-col w-full gap-4">

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
                <button 
                    className="w-full p-3 font-bold text-white rounded-md bg-primary"
                    onClick={handleCreateAccount}
                >
                    Create
                </button>
                <div className="text-[12px]">
                    By creating your account, you agree to our <a href='/terms-and-conditions' className="underline">Terms and Conditions</a> and our <a href='/privacy' className="underline">Privacy Policy</a>.
                </div>
            </div>
        </div>
    )
}


export default CreateAccount