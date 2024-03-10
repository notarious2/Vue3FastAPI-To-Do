import { createApp } from "vue";
import App from "./App.vue";
import router from "./router.js";
import "./axios";
import TheHeader from "@/components/layout/TheHeader.vue";
import TheFooter from "@/components/layout/TheFooter.vue";

import { createPinia } from "pinia";
import VueGtag from "vue-gtag";

const app = createApp(App);

const pinia = createPinia();

app.component("the-header", TheHeader);
app.component("the-footer", TheFooter);

app.use(router);
app.use(VueGtag, { config: { id: import.meta.env.VITE_GA_MEASUREMENT_ID } }); // for google analytics
app.use(pinia);

app.mount("#app");
