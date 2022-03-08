<script lang="ts">
import {
  defineComponent, onMounted, ref, Ref,
} from '@vue/composition-api';
import { Image, Pagination, getMyImages } from '../client';
import ImageList from '../components/ImageList.vue';

export default defineComponent({
  components: {
    ImageList,
  },
  setup() {
    const images = ref(null) as Ref<Pagination<Image> | null>;

    onMounted(async () => {
      images.value = await getMyImages();
    });

    return { images };
  },
});
</script>

<template>
  <v-container>
    <ImageList :images="images" />
  </v-container>
</template>
