import { createRouter, createWebHistory } from "vue-router";

const TheHome = () => import("./pages/TheHome.vue");
const TheLogin = () => import("@/pages/TheLogin.vue");
const TheRegistration = () => import("./pages/TheRegistration.vue");
const TheDemo = () => import("./pages/TheDemo.vue");
const NotFound = () => import("./pages/NotFound.vue");

const routes = [
  {
    path: "/",
    name: "Home",
    component: TheHome,
  },
  {
    path: "/login",
    name: "Authorization",
    component: TheLogin,
  },
  {
    path: "/register",
    name: "Registration",
    component: TheRegistration,
  },
  {
    path: "/demo",
    name: "Demo",
    component: TheDemo,
  },
  {
    path: "/callback/",
    component: () => import("@/pages/GoogleCallback.vue"),
  },
  { path: "/:notFound(.*)", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
