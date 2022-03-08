import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import ImagesPage from '../views/ImagesPage.vue';
import MyImagesPage from '../views/MyImagesPage.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    name: 'home',
    path: '/',
    component: HomePage,
  },
  {
    name: 'images',
    path: '/images',
    component: ImagesPage,
  },
  {
    name: 'my-images',
    path: '/my-images',
    component: MyImagesPage,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
