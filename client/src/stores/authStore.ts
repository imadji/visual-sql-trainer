import { defineStore } from "pinia";
import axios from "axios";

interface Credentials {
  login: string;
  password: string;
}
interface UserDataSql {
  query: string;
  user: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    userLogin: localStorage.getItem("authToken") || null,
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
        this.userLogin = credentials.login;
        localStorage.setItem("authToken", this.userLogin);
      }

      return data;
    },

    async register(credentials: Credentials) {
      const response = await axios.post("http://localhost:8000/auth/reg", credentials, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = response.data;
      if (data.status) {
        this.userLogin = credentials.login;
        localStorage.setItem("authToken", this.userLogin);
      }

      return response.data;
    },

    logout() {
      this.userLogin = null;
      localStorage.removeItem("authToken");
    },
  },
});

export const useSqlRequest = defineStore("sql", {
  actions: {
    async executeSqlReq(command: UserDataSql) {
      const response = await axios.post("http://localhost:8000/sql_query", command, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },
  },
});
