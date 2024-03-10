import axios from "axios";
import { useAuthStore } from "@/store/authStore.js";

// axios interceptor for specific URL - instance
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT,
});


//response interceptor
axiosInstance.interceptors.response.use(
  // If the response is successful, just return it
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    // don't refresh if either access or refresh token is invalid
    if (
      error.response && originalRequest.url.includes("refresh")
    ) {
      const authStore = useAuthStore();
      authStore.logout();
    }
    // refresh token if it is expired
    else if (
      error.response && error.response.status === 401 &&
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
      console.log("Other error");
      return Promise.reject(error);
    }
  }
);
export default axiosInstance;