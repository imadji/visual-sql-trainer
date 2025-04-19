import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView/HomeView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";
import DebuggerView from "../components/DebuggerView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/workspace", component: WorkspaceView },
  {
    path: "/debugger",
    name: "DebuggerView",
    component: DebuggerView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("authToken");
  if (to.meta.requiresAuth && !token) next("/");
  else next();
});

export default router;
