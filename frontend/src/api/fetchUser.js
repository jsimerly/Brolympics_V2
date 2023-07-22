const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchCreateUser(phoneNumber, firstName, lastName, password){
    
    const data={
        password: password,
        first_name : firstName,
        last_name : lastName,
        phone: phoneNumber,
    }

    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/account/create-user/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        });
        return response

    } catch (error) {
        throw error
    }
}

export async function fetchLoginUser(phoneNumber, password){
    const userData ={
        phoneNumber : phoneNumber,
        password: password,
    }

    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/account/token/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify(userData),
        })

        
        const resp = await response.json()
        setCookie('access_token', resp.access, 60);
        setCookie('refresh_token', resp.refresh, 60 * 24 * 30);

        return response

    } catch (error) {
        throw (error)
    }
}

export function handleLogout(){
    deleteCookie('access_token');
    deleteCookie('refresh_token')
    window.location.reload()
}

export async function fetchUserInformation(){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/account/user-information/`)

        return response

    } catch (error) {
        throw error
    }
}

export async function fetchResetPassword(email){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/account/reset-password/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify({email: email}),
        })
        return response
        
    } catch (error) {
        throw error
    }
}

export async function fetchVerifyPhone(phoneNumber, firstName, lastName, password, code){
    const data = {
        phone: phoneNumber,
        first_name: firstName,
        last_name: lastName,
        password: password,
        code: code,
    }
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/account/verify-phone/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        })
        return response
    } catch (error) {
        throw error
    }
}