const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchUpdateEvent(event){
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/update-event/`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
            body: JSON.stringify(event),
        })

        return response

    } catch (error) {
        throw (error)
    }
}