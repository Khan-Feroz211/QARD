/**
 * authStore.js — Zustand store for authentication state.
 */
import { create } from 'zustand';
import { loginStudent, registerStudent, logoutUser } from '../services/auth';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email, password, universitySlug) => {
    const data = await loginStudent(email, password, universitySlug);
    set({ user: data, isAuthenticated: true });
  },

  register: async (form) => {
    const data = await registerStudent(form);
    set({ user: data, isAuthenticated: true });
  },

  logout: async () => {
    await logoutUser();
    set({ user: null, isAuthenticated: false });
  },

  setUser: (user) => set({ user, isAuthenticated: !!user }),
}));
