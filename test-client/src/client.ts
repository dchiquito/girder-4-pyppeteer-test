import axios from 'axios';
import OauthClient from '@girder/oauth-client';
import { Ref, ref } from '@vue/composition-api';

export const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_ROOT,
});

export const oauthClient = new OauthClient(
  process.env.VUE_APP_OAUTH_API_ROOT,
  process.env.VUE_APP_OAUTH_CLIENT_ID,
);

export interface User {
  id: number,
  username: string,
}

export interface Image {
  id: number,
  name: string,
  checksum: string | null;
  created: string,
  modified: string,
  owner: User,
}

export interface Pagination<T> {
  count: number,
  next: string | null,
  previous: string | null,
  results: T[],
}

// this will be initialized to a ref by maybeRestoreLogin before the app is mounted.
// eslint-disable-next-line import/no-mutable-exports
export let currentUser: Ref<User | null> = null as unknown as Ref<User | null>;

export async function maybeRestoreLogin() {
  await oauthClient.maybeRestoreLogin();
  Object.assign(axiosInstance.defaults.headers.common, oauthClient.authHeaders);
  if (currentUser === null) {
    currentUser = ref(null);
  }
  await axiosInstance.get('/users/me/').then((response) => {
    currentUser.value = response.data;
  }, () => {
    // The log in was not restored
  });
}

export async function logout() {
  await axiosInstance.post('/users/logout/');
  await oauthClient.logout();
  currentUser.value = null;
}

export async function getImages(): Promise<Pagination<Image>> {
  return (await axiosInstance.get('/images/')).data;
}

export async function getMyImages(): Promise<Pagination<Image>> {
  return (await axiosInstance.get('/images/', { params: { owner: currentUser.value?.id } })).data;
}

export function getImageUrl(imageId: number): string {
  return `${process.env.VUE_APP_API_ROOT}/images/${imageId}/download/`;
}
