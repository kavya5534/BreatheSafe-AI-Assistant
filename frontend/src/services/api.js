const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const errData = await response.json();
      if (errData?.detail) {
        message = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
      }
    } catch {
      // ignore json parse failure
    }
    throw new Error(message);
  }

  return response.json();
}

export const api = {
  getHealth: () => request('/api/health'),

  getDashboard: ({ city, lang, sessionId }) => {
    const params = new URLSearchParams();
    if (city) params.set('city', city);
    if (lang) params.set('lang', lang);
    if (sessionId) params.set('session_id', sessionId);
    return request(`/api/dashboard?${params.toString()}`);
  },

  getPreferences: (sessionId) => {
    const params = new URLSearchParams({ session_id: sessionId || 'default' });
    return request(`/api/preferences?${params.toString()}`);
  },

  savePreferences: (payload) =>
    request('/api/preferences', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  sendChat: (payload) =>
    request('/api/chat', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getChatHistory: (sessionId) => {
    const params = new URLSearchParams({ session_id: sessionId || 'default' });
    return request(`/api/chat/history?${params.toString()}`);
  },

  clearChatHistory: (sessionId) => {
    const params = new URLSearchParams({ session_id: sessionId || 'default' });
    return request(`/api/chat/history?${params.toString()}`, {
      method: 'DELETE',
    });
  },

  getReports: () => request('/api/reports'),

  createReport: (payload) =>
    request('/api/reports', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  upvoteReport: (reportId) =>
    request(`/api/reports/${reportId}/upvote`, {
      method: 'POST',
    }),

  getActivities: (sessionId) => {
    const params = new URLSearchParams({ session_id: sessionId || 'default' });
    return request(`/api/activities?${params.toString()}`);
  },

  createActivity: (payload) =>
    request('/api/activities', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
