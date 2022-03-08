import axios from 'axios';
import OauthClient from '@girder/oauth-client';

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

export async function getImages(): Promise<Pagination<Image>> {
  return (await axiosInstance.get('/images/')).data;
}

export async function getMyImages(): Promise<Pagination<Image>> {
  return (await axiosInstance.get('/images/')).data;
}

export function getImageUrl(imageId: number): string {
  return `${process.env.VUE_APP_API_ROOT}/images/${imageId}/download/`;
}
