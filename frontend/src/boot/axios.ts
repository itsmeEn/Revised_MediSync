import { defineBoot } from '#q-app/wrappers';
import axios, { type AxiosInstance } from 'axios';

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
const resolveBaseURL = (): string => {
  const override = localStorage.getItem('API_BASE_URL');
  if (override) {
    return override.replace(/\/$/, '');
  }
  const host = window.location.hostname || 'localhost';
  return `http://${host}:8000/api`;
};

const api = axios.create({
  baseURL: resolveBaseURL()
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');

    // Avoid attaching tokens to auth-related endpoints
    const url = config.url || '';
    const isAuthEndpoint =
      url.includes('/users/login/') ||
      url.includes('/users/register/') ||
      url.includes('/users/forgot-password/') ||
      url.includes('/users/reset-password') ||
      url.includes('/users/token/refresh/');

    if (token && !isAuthEndpoint) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 Adding auth token to request:', config.url);
    } else if (!token) {
      console.warn('⚠️ No access token found for request:', config.url);
    } else if (isAuthEndpoint) {
      console.log('🚫 Skipping auth header for auth endpoint:', config.url);
    }

    return config;
  },
  (error) => {
    return Promise.reject(new Error(error.message || 'Request failed'));
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Do not attempt refresh on auth endpoints
    const url = originalRequest?.url || '';
    const isAuthEndpoint =
      url.includes('/users/login/') ||
      url.includes('/users/register/') ||
      url.includes('/users/forgot-password/') ||
      url.includes('/users/reset-password') ||
      url.includes('/users/token/refresh/');

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      console.log('🔄 401 Unauthorized detected, attempting token refresh...');
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          console.log('📤 Attempting to refresh token...');
          const response = await axios.post(`${api.defaults.baseURL}/users/token/refresh/`, {
            refresh: refreshToken
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);
          console.log('✅ Token refreshed successfully');

          originalRequest.headers.Authorization = `Bearer ${access}`;
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

    return Promise.reject(new Error(error.message || 'Response failed'));
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
