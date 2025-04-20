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

interface RequestTaskData {
  query: string;
  user: string;
  task_id: number;
}

interface TableData {
  name: string;
  headers: string[];
  data: any[][];
  position: { x: number; y: number };
  width: number;
  isDragging: boolean;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    userLogin: localStorage.getItem("authToken") || null,
    tables: [] as TableData[],
    allTables: [] as TableData[],
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

    async getAllTables(login: string) {
      const response = await axios.get("http://localhost:8000/auth/get_tables", {
        params: { login },
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },

    setTables(tables: TableData[]) {
      this.tables = tables;
    },

    logout() {
      this.userLogin = null;
      localStorage.removeItem("authToken");
    },
  },
});

export const useAIrequest = defineStore("ai", {
  actions: {
    async genTask(tables: any) {
      const response = await axios.post("http://localhost:8000/gen-sql-task", tables, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
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
    async executeSqlStep(command: UserDataSql) {
      const response = await axios.post(
        "http://localhost:8000/sql_query/query_processing",
        command,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      return response.data;
    },
  },
});

export const useTaskRequest = defineStore("task", {
  actions: {
    async getAllTask(user_login: string) {
      const response = await axios.get("http://localhost:8000/sql_task/get_tasks", {
        params: { user_login },
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },
    async checkSolveTask(command: RequestTaskData) {
      const response = await axios.post("http://localhost:8000/sql_task/solve_task", command, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },
  },
});
