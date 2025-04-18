import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("authToken") || null,
  }),
  actions: {
    async login(credentials: string) {
      const response = await fetch("https://api.example.com/login", {
        method: "POST",
        body: JSON.stringify(credentials),
      });
      const data = await response.json();
      this.token = data.token;
      localStorage.setItem("authToken", data.token);
    },
    logout() {
      this.token = null;
      localStorage.removeItem("authToken");
    },
  },
});
