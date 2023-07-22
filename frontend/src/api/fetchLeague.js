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