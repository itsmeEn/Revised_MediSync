import { defineBoot } from '#q-app/wrappers';
import axios, { type AxiosInstance, type AxiosError, type AxiosRequestConfig, type RawAxiosRequestHeaders } from 'axios';

declare module 'vue' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 Adding auth token to request:', config.url);
    } else {
      console.warn('⚠️ No access token found for request:', config.url);
    }
    return config;
  },
  (error: unknown) => {
    // Ensure we reject with an Error instance to satisfy ESLint rule
    const reason = error instanceof Error ? error : new Error(String(error));
    return Promise.reject(reason);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('🔄 401 Unauthorized detected, attempting token refresh...');
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          console.log('📤 Attempting to refresh token...');
          const response = await axios.post('http://localhost:8000/api/users/token/refresh/', {
            refresh: refreshToken
          });

          const { access } = response.data as { access: string };
          localStorage.setItem('access_token', access);
          console.log('✅ Token refreshed successfully');

          const headers = (originalRequest.headers || {}) as RawAxiosRequestHeaders;
          headers['Authorization'] = `Bearer ${access}`;
          originalRequest.headers = headers;
          return api(originalRequest);
        } else {
          console.warn('⚠️ No refresh token found');
        }
      } catch (refreshError) {
        console.error('❌ Token refresh failed:', refreshError);
        // Refresh token failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    // Ensure we reject with an Error instance to satisfy ESLint rule
    const reason = error instanceof Error ? error : new Error(String(error));
    return Promise.reject(reason);
  }
);

export default defineBoot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
