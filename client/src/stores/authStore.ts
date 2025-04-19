import { defineStore } from "pinia";
import axios from "axios";

interface Credentials {
  login: string;
  password: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("authToken") || null,
  }),

  actions: {
    async login(credentials: Credentials) {
      const response = await axios.post("http://localhost:8000/auth/login", credentials, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = response.data;

      if (data.status) {
        this.token = "generated-token"; // в будущем будет токен
        localStorage.setItem("authToken", this.token);
      }

      return data;
    },

    async register(credentials: Credentials) {
      const response = await axios.post("http://localhost:8000/auth/reg", credentials, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      return response.data;
    },

    logout() {
      this.token = null;
      localStorage.removeItem("authToken");
    },
  },
});

export const useSqlRequest = defineStore("sql", {
  actions: {
    async executeSqlReq(command: string) {
      const response = await axios.post("http://localhost:8000/sql/execute", command, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },
  },
});
