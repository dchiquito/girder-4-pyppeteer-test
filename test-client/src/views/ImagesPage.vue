<script lang="ts">
import {
  defineComponent, onMounted, ref, Ref,
} from '@vue/composition-api';
import { Image, Pagination, getImages } from '../client';
import ImageList from '../components/ImageList.vue';

export default defineComponent({
  components: {
    ImageList,
  },
  setup() {
    const images = ref(null) as Ref<Pagination<Image> | null>;

    onMounted(async () => {
      images.value = await getImages();
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
