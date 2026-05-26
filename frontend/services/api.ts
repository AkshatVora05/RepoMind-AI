import axios from 'axios';
import { RepoResponse, QueryResponse } from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ingestRepository = async (url: string): Promise<RepoResponse> => {
  const response = await apiClient.post('/repos/ingest', { url });
  return response.data;
};

export const getRepository = async (repoId: string): Promise<RepoResponse> => {
  const response = await apiClient.get(`/repos/${repoId}`);
  return response.data;
};

export const deleteRepository = async (repoId: string): Promise<void> => {
  await apiClient.delete(`/repos/${repoId}`);
};

export const queryRepository = async (repoId: string, query: string): Promise<QueryResponse> => {
  const response = await apiClient.post(`/query/${repoId}`, { query });
  return response.data;
};
