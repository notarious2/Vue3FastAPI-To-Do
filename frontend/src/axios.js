import axios from "axios";
import { useAuthStore } from "../src/components/store/userAuth.js";

axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;
// axios interceptor for specific URL - instance

//response interceptor
axios.interceptors.response.use(
  (res) => {
    return res;
  },
  async function (error) {
    console.log("Error", error);
    const originalRequest = error.config;
    // don't refresh if either access or refresh token is invalid
    if (
      error.response.status === 401 &&
      (error.response.data.detail === "Invalid Access Token" ||
        error.response.data.detail === "Invalid Refresh Token")
    ) {
      const authStore = useAuthStore();
      authStore.logout();
    }
    // refresh token if it is expired
    else if (
      error.response.status === 401 &&
      error.response.data.detail === "Token expired" &&
      error.request.responseURL.includes(axios.defaults.baseURL) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const authStore = useAuthStore();
      // get newly assigned access token
      const newAccessToken = await authStore.refreshToken();
      // retry original request
      originalRequest.headers["Authorization"] = "Bearer " + newAccessToken;
      return axios.request(originalRequest);
    } else {
      // some other error
      location.reload();
      return Promise.reject(error);
    }
  }
);
