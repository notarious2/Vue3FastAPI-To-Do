<template>
  <the-header></the-header>
  <main>
    <h1>Welcome to the to-do list app</h1>
    <h2>Simple, yet powerful task management application</h2>
    <div class="swip">
      <swiper
        :slidesPerView="1"
        :spaceBetween="30"
        :loop="true"
        :lazy="true"
        :centeredSlides="true"
        :pagination="{
          clickable: true,
        }"
        :autoplay="{
          delay: 5000,
          // disableOnInteraction: false,
        }"
        :navigation="true"
        :modules="modules"
      >
        <swiper-slide
          ><img
            :src="require('../assets/tasks_slide_1.webp')"
            alt="slide 1"
            class="slide-1 swiper-lazy"
            rel="preload"
        /></swiper-slide>
        <swiper-slide
          ><img
            :src="require('../assets/tasks_slide_2.webp')"
            alt="slide 2"
            class="slide-2 swiper-lazy"
            rel="preload"
        /></swiper-slide>
        <swiper-slide
          ><img
            :src="require('../assets/tasks_slide_3.webp')"
            alt="slide 3"
            class="slide-3 swiper-lazy"
            rel="preload" /></swiper-slide
      ></swiper>
      <div class="linksbox">
        <post-it id="registration-form">
          <div class="inner-registration-form">
            <p><strong> Try Demo. No registration required! </strong></p>
            <button
              @click="
                router.push({ name: 'Demo' });
                demoAnalytics();
              "
              class="button-74"
            >
              Demo
            </button>
          </div>
        </post-it>
        <post-it id="registration-form">
          <div class="inner-registration-form">
            <p><strong> Join for Free </strong></p>
            <button
              @click="
                router.push({ name: 'Registration' });
                registerAnalytics();
              "
              class="button-74"
            >
              Register
            </button>
          </div>
        </post-it>
      </div>
    </div>
  </main>
  <the-footer class="footer"></the-footer>
</template>

<script setup>
import { ref } from "vue";
import { Swiper, SwiperSlide } from "swiper/vue";
import PostIt from "../components/layout/PostIt.vue";
import { event } from "vue-gtag";

import SwiperCore, {
  Navigation,
  Pagination,
  Scrollbar,
  A11y,
  Autoplay,
  Lazy,
} from "swiper";

import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/autoplay";
import "swiper/css/lazy";

import { useRouter } from "vue-router";

SwiperCore.use([Navigation, Pagination, Scrollbar, A11y, Autoplay, Lazy]);
const modules = ref([Navigation, Pagination, Scrollbar, A11y, Autoplay, Lazy]);
const router = useRouter();

function demoAnalytics() {
  event("demo-button-clicked", {
    event_category: "analytics",
    event_label: "Demo button pressed",
    value: 1,
  });
}
function registerAnalytics() {
  event("register-button-clicked", {
    event_category: "analytics",
    event_label: "Register button pressed",
    value: 1,
  });
}
</script>

<style scoped>
* {
  font-family: "Kalam", cursive;
}
.slide-1 {
  width: 90%;
  height: 50%;
}
.slide-2 {
  width: 70%;
  height: 70%;
}
.slide-3 {
  width: 50%;
  height: 50%;
  margin-bottom: 15px;
}
.linksbox {
  display: flex;
}
#registration-form {
  display: flex;
  width: 70%;
  justify-content: center;
  align-items: center;

  padding: 0px;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 3rem;
}

.inner-registration-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}
main {
  display: flex;
  flex-direction: column;
  min-height: 90vh;
}
.footer {
  margin-top: auto;
}
.button-74 {
  background-color: #fbeee0;
  border: 2px solid #422800;
  border-radius: 25px;
  box-shadow: #422800 3px 3px 0 0;
  color: #422800;
  cursor: pointer;
  font-weight: 300;
  font-size: 16px;
  padding: 3px 18px;
  line-height: 20px;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  flex: 0;
  flex-basis: 40px;
  padding: 0px 20px;
}
</style>

<style>
.swiper-button-next,
.swiper-button-prev {
  color: lightsalmon;
  height: 0px;
  width: 15px;
}
</style>

<style>
.swiper-pagination-bullet {
  margin-right: 5px !important;
}
</style>
