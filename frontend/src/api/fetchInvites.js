const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;
import { deleteCookie, fetchWrapper, getCookie, setCookie } from "./cookies";

export async function fetchLeagueInviteInfo(uuid){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/league-invite/${uuid}`)

        return response

    } catch (error) {
        throw error
    }
}

export async function fetchJoinLeague(uuid){

    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/join-league/${uuid}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
        })

        return response

    } catch (error) {
        throw (error)
    }
}

export async function fetchBrolympicsInvite(uuid){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/brolympics-invite/${uuid}`)

        return response

    } catch (error) {
        throw error
    }
}

export async function fetchJoinBrolympics(uuid){

    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/join-brolympics/${uuid}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
        })

        return response

    } catch (error) {
        throw (error)
    }
}

export async function fetchTeamInvite(uuid){
    try {
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/team-invite/${uuid}`)

        return response

    } catch (error) {
        throw error
    }
}

export async function fetchJoinTeam(uuid){

    try{
        const response = await fetchWrapper(`${SERVER_ADDRESS}/api/brolympics/team-brolympics/${uuid}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN' : getCookie('csrftoken'),
            },
        })

        return response

    } catch (error) {
        throw (error)
    }
}