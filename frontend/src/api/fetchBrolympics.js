const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchBrolympicsHome(uuid){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/get-brolympics-home/${uuid}`)

        return response
        
    } catch (error) {
        throw error
    }
}

export async function fetchInCompetition(){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/is-in-competition/`)

        return response
        
    } catch (error) {
        throw error
    }
}