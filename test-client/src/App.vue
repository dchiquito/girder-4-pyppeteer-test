<script lang="ts">
import { defineComponent, inject, computed } from '@vue/composition-api';
import OAuthClient from '@girder/oauth-client';

export default defineComponent({
  setup() {
    const oauthClient = inject<OAuthClient>('oauthClient');
    if (oauthClient === undefined) {
      throw new Error('Must provide "oauthClient" into component.');
    }

    const loginText = computed(() => (oauthClient.isLoggedIn ? 'Logout' : 'Login'));
    const logInOrOut = () => {
      if (oauthClient.isLoggedIn) {
        oauthClient.logout();
      } else {
        oauthClient.redirectToLogin();
      }
    };

    return { oauthClient, loginText, logInOrOut };
  },
});
</script>

<template>
  <v-app>
    <v-app-bar app>
      <v-tabs>
        <v-tab :to="{name: 'home'}">
          Home
        </v-tab>
        <v-tab :to="{name: 'images'}">
          All Images
        </v-tab>
        <v-tab
          v-if="oauthClient.isLoggedIn"
          :to="{name: 'my-images'}"
        >
          My Images
        </v-tab>
      </v-tabs>
      <v-spacer />
      <v-btn
        text
        @click="logInOrOut"
      >
        {{ loginText }}
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
