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

export async function fetchLeagueInfo(uuid){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/league-info/${uuid}`)

        return response
    } catch (error) {
        throw error
    }
}

export async function createAllLeague(league, brolympics, h2h, ind, team){
    const data = {
        league: league,
        brolympics: brolympics,
        h2h_event: h2h,
        ind_event: ind,
        team_event: team,
    }
    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/create-all-league/`,
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