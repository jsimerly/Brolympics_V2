const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchUpdateEvent(event){
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/create-all-league/`,
        {
            method: 'POST',
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

export async function fetchCreateEvent(event, type, uuid){
    const data = {'event_name' : event, 'type': type, 'uuid':uuid}
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/create-event/`,
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
        throw (error)
    }
}