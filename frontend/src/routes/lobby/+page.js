import axios from 'axios';

export const load = async ({fetch, data}) => {

    

    let response = await axios.get("http://localhost:8000/fx/stocks/", {withCredentials: true})
    if (response.status === 200)
    {
        return { stockData: response.data };
    }

    
}