<script lang="ts">
import moment from 'moment';
import {
  defineComponent, inject, computed, PropType, watch, watchEffect,
} from '@vue/composition-api';
import { Image, Pagination, getImageUrl } from '../client';

export default defineComponent({
  props: {
    images: {
      type: Object as PropType<Pagination<Image> | null>,
      default: null,
    },
  },
  setup() {
    function formatDate(dateString: string) {
      return moment(dateString).format('MMMM DD YYYY');
    }
    return {
      formatDate,
      getImageUrl,
    };
  },
});
</script>

<template>
  <v-container>
    <v-list v-if="images">
      <v-list-item
        v-for="image in images.results"
        :key="image.id"
      >
        <v-card>
          <v-card-title>{{ image.name }}</v-card-title>
          <v-card-subtitle>
            <div>
              {{ image.owner.username }}
            </div>
            <v-spacer />
            <div>
              {{ formatDate(image.created) }}
            </div>
            <div v-if="image.checksum">
              {{ image.checksum }}
            </div>
          </v-card-subtitle>
          <v-img :src="getImageUrl(image.id)" />
        </v-card>
      </v-list-item>
    </v-list>
    <v-progress-circular
      v-else
      indeterminate
    />
  </v-container>
</template>
