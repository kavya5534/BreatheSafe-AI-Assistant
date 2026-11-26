import { useState } from 'react';

const STORAGE_KEY = 'breathesafe_session_id';

export function useSessionId() {
  const [sessionId] = useState(() => {
    try {
      const existing = localStorage.getItem(STORAGE_KEY);
      if (existing) return existing;
      const created = 'bs_' + Math.random().toString(36).slice(2, 10);
      localStorage.setItem(STORAGE_KEY, created);
      return created;
    } catch {
      return 'default';
    }
  });

  return sessionId;
}
