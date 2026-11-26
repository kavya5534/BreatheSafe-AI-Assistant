import { useEffect, useState } from 'react';
import { CheckCircle2, Save, SlidersHorizontal } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';
import { api } from '../services/api';
import { LANGUAGE_OPTIONS } from '../translations';

export function PreferencesPage({ sessionId, onPreferencesSaved }) {
  const { language, setLanguage, t } = useLanguage();
  const [form, setForm] = useState({
    location: 'Bengaluru',
    preferred_language: language,
    age_group: 'adult',
    lifestyle: 'balanced',
    family_categories: ['general'],
    transportation_type: 'public_transit',
    outdoor_preferences: ['morning_walk'],
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    api
      .getPreferences(sessionId)
      .then((res) => {
        if (!active) return;
        setForm({
          location: res.location || 'Bengaluru',
          preferred_language: res.preferred_language || language,
          age_group: res.age_group || 'adult',
          lifestyle: res.lifestyle || 'balanced',
          family_categories: res.family_categories || ['general'],
          transportation_type: res.transportation_type || 'public_transit',
          outdoor_preferences: res.outdoor_preferences || ['morning_walk'],
        });
      })
      .catch((err) => {
        if (active) setError(err.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [sessionId]);

  const toggleMulti = (field, value) => {
    setForm((prev) => {
      const current = prev[field] || [];
      const exists = current.includes(value);
      const next = exists ? current.filter((item) => item !== value) : [...current, value];
      return { ...prev, [field]: next.length ? next : [value] };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSavedMsg('');
    setError('');
    try {
      const saved = await api.savePreferences({
        session_id: sessionId,
        ...form,
      });
      setLanguage(saved.preferred_language);
      setSavedMsg(t.preferences.savedNotice);
      if (onPreferencesSaved) {
        onPreferencesSaved(saved);
      }
    } catch (err) {
      setError(err.message || 'Failed to save preferences');
    } finally {
      setSaving(false);
    }
  };

  const ageKeys = ['child', 'teen', 'adult', 'senior'];
  const lifestyleKeys = ['sedentary', 'balanced', 'active', 'outdoor_worker'];
  const transportKeys = ['walking', 'cycling', 'public_transit', 'two_wheeler', 'car', 'ev'];
  const familyKeys = ['general', 'children', 'elderly', 'pregnant', 'respiratory_sensitive'];
  const outdoorKeys = ['morning_walk', 'evening_jog', 'cycling', 'gardening', 'sports', 'mostly_indoor'];

  if (loading) {
    return <div className="glass-panel rounded-2xl p-8 text-sky-200">{t.common.loading}</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2.5">
          <SlidersHorizontal className="h-7 w-7 text-emerald-400" />
          {t.preferences.title}
        </h2>
        <p className="text-sm text-sky-200/80 mt-1">{t.preferences.subtitle}</p>
      </div>

      {error && (
        <div className="rounded-xl bg-red-500/15 border border-red-400/40 px-4 py-3 text-sm text-red-200">
          {t.common.errorPrefix}: {error}
        </div>
      )}

      {savedMsg && (
        <div className="rounded-xl bg-emerald-500/15 border border-emerald-400/40 px-4 py-3 flex items-center gap-2 text-sm text-emerald-200">
          <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
          <span>{savedMsg}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="glass-panel rounded-2xl p-5 sm:p-7 space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2">
              {t.preferences.locationLabel}
            </label>
            <input
              type="text"
              required
              value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2">
              {t.preferences.languageLabel}
            </label>
            <select
              value={form.preferred_language}
              onChange={(e) => setForm({ ...form, preferred_language: e.target.value })}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
            >
              {LANGUAGE_OPTIONS.map((opt) => (
                <option key={opt.code} value={opt.code}>
                  {opt.nativeLabel} ({opt.label})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2">
              {t.preferences.ageGroupLabel}
            </label>
            <select
              value={form.age_group}
              onChange={(e) => setForm({ ...form, age_group: e.target.value })}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
            >
              {ageKeys.map((key) => (
                <option key={key} value={key}>
                  {t.preferences.options.ageGroup[key]}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2">
              {t.preferences.lifestyleLabel}
            </label>
            <select
              value={form.lifestyle}
              onChange={(e) => setForm({ ...form, lifestyle: e.target.value })}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
            >
              {lifestyleKeys.map((key) => (
                <option key={key} value={key}>
                  {t.preferences.options.lifestyle[key]}
                </option>
              ))}
            </select>
          </div>

          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2">
              {t.preferences.transportLabel}
            </label>
            <select
              value={form.transportation_type}
              onChange={(e) => setForm({ ...form, transportation_type: e.target.value })}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
            >
              {transportKeys.map((key) => (
                <option key={key} value={key}>
                  {t.preferences.options.transport[key]}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Multi-select: Family categories */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2.5">
            {t.preferences.familyLabel}
          </label>
          <div className="flex flex-wrap gap-2.5">
            {familyKeys.map((key) => {
              const selected = form.family_categories.includes(key);
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => toggleMulti('family_categories', key)}
                  className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium border transition cursor-pointer ${
                    selected
                      ? 'bg-emerald-500/20 text-emerald-200 border-emerald-400'
                      : 'bg-slate-900/80 text-slate-300 border-slate-700 hover:border-sky-400/40'
                  }`}
                >
                  {t.preferences.options.family[key]}
                </button>
              );
            })}
          </div>
        </div>

        {/* Multi-select: Outdoor preferences */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-sky-300 mb-2.5">
            {t.preferences.outdoorLabel}
          </label>
          <div className="flex flex-wrap gap-2.5">
            {outdoorKeys.map((key) => {
              const selected = form.outdoor_preferences.includes(key);
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => toggleMulti('outdoor_preferences', key)}
                  className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium border transition cursor-pointer ${
                    selected
                      ? 'bg-sky-400/20 text-sky-200 border-sky-400'
                      : 'bg-slate-900/80 text-slate-300 border-slate-700 hover:border-sky-400/40'
                  }`}
                >
                  {t.preferences.options.outdoor[key]}
                </button>
              );
            })}
          </div>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm transition cursor-pointer disabled:opacity-50"
        >
          <Save className="h-4 w-4" />
          {saving ? t.common.saving : t.preferences.saveBtn}
        </button>
      </form>
    </div>
  );
}
