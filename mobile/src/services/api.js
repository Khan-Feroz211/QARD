/**
 * api.js — Axios instance with base URL and JWT auth interceptor.
 */
import axios from 'axios';
import { getToken } from './storage';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://10.0.2.2:8000/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(async (config) => {
  const token = await getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired – optionally trigger a global logout here
    }
    return Promise.reject(error);
  },
);
