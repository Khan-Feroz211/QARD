/**
 * cardStore.js — Zustand store for virtual card state.
 */
import { create } from 'zustand';
import { api } from '../services/api';

export const useCardStore = create((set) => ({
  card: null,
  loading: false,
  error: null,

  fetchCard: async () => {
    set({ loading: true, error: null });
    try {
      const response = await api.get('/card');
      set({ card: response.data, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  regenerateCard: async () => {
    set({ loading: true });
    try {
      const response = await api.put('/card/regenerate');
      set({ card: response.data, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },
}));
