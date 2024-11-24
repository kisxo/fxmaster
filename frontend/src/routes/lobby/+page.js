import Cookies from 'js-cookie';
import axios from 'axios';
import { goto, replaceState } from '$app/navigation';

console.log("outside")

export const load = async ({fetch, data}) => {
    let stockData = [];
    let isAllowed = false;

    try {
        const res = await axios.get('http://localhost:8000/_allauth/browser/v1/auth/session', {withCredentials: true})

        console.log("lobby login check")
        console.log(res)

        if(res.status === 200)
        {
           isAllowed = true
        }
         
    } catch (error) {
        
    }

    try {
        const res = await axios.get('http://localhost:8000/fx/stocks/', {withCredentials: true})

        if(res.status === 200)
        {
            stockData = res.data;
        }

        
    } catch (error) {
        console.error("get stockdata error")
    }

    return {
        isAllowed: isAllowed,
        stockData: stockData
    }

}