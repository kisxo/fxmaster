export const ssr = false;
export const prerender = true;

import Cookies from "js-cookie";
import axios from "axios";

axios.interceptors.request.use(
    async function (config) {
        config.headers["X-CSRFToken"] = Cookies.get('csrftoken');
        console.log("intercept\n\n")
        return config;
    },
    function (error) {
      return Promise.reject(error);
    }
);