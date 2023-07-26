const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "../cookies";

export async function fetchStartBrolympics(uuid){
    const data = {uuid: uuid}
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/start-brolympics/`,
        {
            method: 'PUT',
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

export async function fetchEventsUnstarted(uuid){
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/events-unstarted/${uuid}`)
        return response
    } catch (error) {
        throw (error)
    }
}