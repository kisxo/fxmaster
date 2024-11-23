export const load = async ({fetch, data}) => {

    const res = await fetch("http://localhost:8000/fx/stocks/")
    const extData = await res.json();
    return {stockData: extData.data};
    
}