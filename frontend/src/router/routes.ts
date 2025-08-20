import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  },
  {
    path: '/forgot-password',
    component: () => import('pages/ForgotPasswordPage.vue')
  },
  {
    path: '/reset-password/:uidb64/:token',
    component: () => import('pages/ResetPasswordPage.vue')
  },
  {
    path: '/role-selection',
    component: () => import('pages/RoleSelectionPage.vue')
  },
  {
    path: '/register/:role',
    component: () => import('pages/RegisterPage.vue')
  },
  {
    path: '/verification',
    component: () => import('pages/VerificationPage.vue')
  },
  {
    path: '/doctor-dashboard',
    component: () => import('pages/DoctorDashboard.vue')
  },
  {
    path: '/nurse-dashboard',
    component: () => import('pages/NurseDashboard.vue')
  },
  {
    path: '/patient-dashboard',
    component: () => import('pages/PatientDashboard.vue')
  },
  {
    path: '/home',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
