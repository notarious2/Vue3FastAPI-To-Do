import { defineStore } from "pinia";
import axios from "@/axios";
import router from "@/router.js";
import { trackUserLoggedInGA, trackUserRegistrationGA } from '@/gaUtils';


export const useAuthStore = defineStore("authentication", {
  state: () => ({
    token: "",
    // initialize state from local storage to enable user to stay logged in
    // user: JSON.parse(localStorage.getItem("user")),
    errorLogIn: false,
    errorMessage: "",
    isAuthenticated: false,
    errorRegister: false,
  }),
  actions: {
    async login(username, password) {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const headers = {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      };
      await axios
        .post("user/jwt/create/", params, {
          headers: headers,
        })
        .then((response) => {
          // store user details and jwt in local storage to keep user logged in between page refreshes
          localStorage.setItem("user", JSON.stringify(response.data));
          // update pinia state
          this.token = response.data["access"];
          this.isAuthenticated = true;
          router.push({ name: "Home" });
          trackUserLoggedInGA();

        })
        .catch((error) => {
          console.log(error);
          this.errorLogIn = true;
          // catching connection refused error
          if (error.message === "Network Error") {
            this.errorMessage = error.message;
          } else {
            this.errorMessage = "Incorrect username/email or password";
          }
        });
    },
    async register(payload) {
      await axios
        .post("users/register/", payload, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          console.log(
            `User ${response.data.username} has been successfully created!`
          );
          router.push({ name: "Authorization" });
          trackUserRegistrationGA();
        })
        .catch((error) => {
          console.log(error);
          this.errorRegister = error.response.data.detail;
        });
    },
    logout() {
      this.token = null;
      localStorage.removeItem("user");
      this.isAuthenticated = false;
      location.reload();
    },

    async refreshToken() {
      var user = localStorage.getItem("user");
      user = JSON.parse(user);
      const refresh = user["refresh_token"];
      localStorage.removeItem("user");

      const response = await axios.post("user/jwt/refresh/", {
        refresh_token: refresh,
      });
      // reassign user in local storage
      user["access_token"] = response.data.access_token;
      user["refresh_token"] = response.data.access_token;
      localStorage.setItem("user", JSON.stringify(user));
      return response.data.access_token;
    },

    clearError() {
      this.errorLogIn = false;
    },
  },
});
