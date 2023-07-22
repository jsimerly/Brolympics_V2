const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchLeagues(){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/all-leagues`)

        return response

    } catch (error) {
        throw error
    }
}

export async function createAllLeague(data){
    const dataa = {data}
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/create-all-league/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify(userData),
        })

        return response

    } catch (error) {
        throw (error)
    }
}