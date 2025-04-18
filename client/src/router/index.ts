import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/workspace", component: WorkspaceView, meta: { requiresAuth: true } },
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
