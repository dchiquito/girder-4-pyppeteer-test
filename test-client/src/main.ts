import * as Sentry from '@sentry/vue';
import Vue from 'vue';
import VueCompositionAPI from '@vue/composition-api';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import { axiosInstance, oauthClient } from './client';

Vue.use(VueCompositionAPI);

Sentry.init({
  Vue,
  dsn: process.env.VUE_APP_SENTRY_DSN,
});

oauthClient.maybeRestoreLogin().then(async () => {
  Object.assign(axiosInstance.defaults.headers.common, oauthClient.authHeaders);

  new Vue({
    provide: {
      axios: axiosInstance,
      oauthClient,
    },
    router,
    vuetify,
    render: (h) => h(App),
  }).$mount('#app');
});
