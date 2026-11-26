import { useEffect, useState } from 'react';
import { Leaf, MapPin, Megaphone, ThumbsUp } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';
import { api } from '../services/api';

export function CommunityPage({ sessionId }) {
  const { t } = useLanguage();
  const [reports, setReports] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [reportForm, setReportForm] = useState({
    reporter_name: '',
    location: '',
    category: 'smoke',
    severity: 'moderate',
    description: '',
  });
  const [submittingReport, setSubmittingReport] = useState(false);

  const [activityForm, setActivityForm] = useState({
    activity_type: 'public_transit',
    description: '',
  });
  const [submittingActivity, setSubmittingActivity] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [repData, actData] = await Promise.all([
        api.getReports(),
        api.getActivities(sessionId),
      ]);
      setReports(repData || []);
      setActivities(actData || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [sessionId]);

  const handleReportSubmit = async (e) => {
    e.preventDefault();
    setSubmittingReport(true);
    setError('');
    try {
      const created = await api.createReport(reportForm);
      setReports((prev) => [created, ...prev]);
      setReportForm({
        reporter_name: '',
        location: '',
        category: 'smoke',
        severity: 'moderate',
        description: '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmittingReport(false);
    }
  };

  const handleUpvote = async (id) => {
    try {
      const updated = await api.upvoteReport(id);
      setReports((prev) => prev.map((r) => (r.id === id ? updated : r)));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleActivitySubmit = async (e) => {
    e.preventDefault();
    setSubmittingActivity(true);
    setError('');
    try {
      const created = await api.createActivity({
        session_id: sessionId,
        ...activityForm,
      });
      setActivities((prev) => [created, ...prev]);
      setActivityForm({ activity_type: 'public_transit', description: '' });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmittingActivity(false);
    }
  };

  const totalCo2 = activities.reduce((acc, a) => acc + (a.co2_saved_kg || 0), 0).toFixed(1);
  const totalPoints = activities.reduce((acc, a) => acc + (a.points || 0), 0);

  const severityBadgeColor = {
    low: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/30',
    moderate: 'bg-sky-400/15 text-sky-300 border-sky-400/30',
    high: 'bg-amber-500/15 text-amber-300 border-amber-400/30',
    critical: 'bg-red-500/15 text-red-300 border-red-400/30',
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {t.community.title}
        </h2>
        <p className="text-sm text-sky-200/80 mt-1">{t.community.subtitle}</p>
      </div>

      {error && (
        <div className="rounded-xl bg-red-500/15 border border-red-400/40 px-4 py-3 text-sm text-red-200">
          {t.common.errorPrefix}: {error}
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Left Column: Community Pollution Reports */}
        <div className="space-y-5">
          <form onSubmit={handleReportSubmit} className="glass-panel rounded-2xl p-5 sm:p-6 space-y-4">
            <div className="flex items-center gap-2">
              <Megaphone className="h-5 w-5 text-sky-300" />
              <h3 className="text-lg font-bold text-white">{t.community.reportFormTitle}</h3>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.reporterName}
                </label>
                <input
                  type="text"
                  required
                  minLength={2}
                  value={reportForm.reporter_name}
                  onChange={(e) => setReportForm({ ...reportForm, reporter_name: e.target.value })}
                  placeholder={t.community.reporterPlaceholder}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.locationLabel}
                </label>
                <input
                  type="text"
                  required
                  minLength={2}
                  value={reportForm.location}
                  onChange={(e) => setReportForm({ ...reportForm, location: e.target.value })}
                  placeholder={t.community.locationPlaceholder}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.categoryLabel}
                </label>
                <select
                  value={reportForm.category}
                  onChange={(e) => setReportForm({ ...reportForm, category: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                >
                  {Object.keys(t.community.categories).map((cat) => (
                    <option key={cat} value={cat}>
                      {t.community.categories[cat]}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.severityLabel}
                </label>
                <select
                  value={reportForm.severity}
                  onChange={(e) => setReportForm({ ...reportForm, severity: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                >
                  {Object.keys(t.community.severities).map((sev) => (
                    <option key={sev} value={sev}>
                      {t.community.severities[sev]}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.community.descriptionLabel}
              </label>
              <textarea
                required
                minLength={8}
                rows={3}
                value={reportForm.description}
                onChange={(e) => setReportForm({ ...reportForm, description: e.target.value })}
                placeholder={t.community.descriptionPlaceholder}
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
              />
            </div>

            <button
              type="submit"
              disabled={submittingReport}
              className="px-5 py-2.5 rounded-xl bg-sky-400 hover:bg-sky-300 text-slate-950 font-bold text-sm transition cursor-pointer disabled:opacity-50"
            >
              {submittingReport ? t.common.saving : t.community.submitReport}
            </button>
          </form>

          {/* Feed */}
          <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-3.5">
            <h3 className="text-base sm:text-lg font-bold text-white">{t.community.feedTitle}</h3>
            {loading ? (
              <p className="text-sm text-slate-400">{t.common.loading}</p>
            ) : reports.length === 0 ? (
              <p className="text-sm text-slate-400">{t.community.noReports}</p>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
                {reports.map((rep) => (
                  <div
                    key={rep.id}
                    className="rounded-xl bg-slate-900/85 border border-slate-800 p-4 space-y-2"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="inline-flex items-center gap-1.5 text-sm font-bold text-white">
                        <MapPin className="h-3.5 w-3.5 text-emerald-400" />
                        {rep.location}
                      </span>
                      <span
                        className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${
                          severityBadgeColor[rep.severity] || severityBadgeColor.moderate
                        }`}
                      >
                        {t.community.severities[rep.severity] || rep.severity}
                      </span>
                    </div>
                    <p className="text-xs font-medium text-sky-300">
                      {t.community.categories[rep.category] || rep.category}
                    </p>
                    <p className="text-sm text-slate-200">{rep.description}</p>
                    <div className="flex items-center justify-between pt-1 text-xs text-slate-400">
                      <span>
                        {rep.reporter_name} • {new Date(rep.created_at).toLocaleDateString()}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleUpvote(rep.id)}
                        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-200 hover:text-emerald-300 transition cursor-pointer"
                      >
                        <ThumbsUp className="h-3 w-3" />
                        <span>
                          {t.community.upvote} ({rep.upvotes})
                        </span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Sustainable Activity Tracker */}
        <div className="space-y-5">
          <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-4">
            <div className="flex items-center gap-2">
              <Leaf className="h-5 w-5 text-emerald-400" />
              <div>
                <h3 className="text-lg font-bold text-white">{t.community.ecoTitle}</h3>
                <p className="text-xs text-slate-400">{t.community.ecoSubtitle}</p>
              </div>
            </div>

            {/* Eco Stats */}
            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-xl bg-emerald-500/10 border border-emerald-400/25 p-3 text-center">
                <p className="text-xs text-emerald-300">{t.community.totalCo2}</p>
                <p className="text-lg font-extrabold text-white mt-0.5">{totalCo2} kg</p>
              </div>
              <div className="rounded-xl bg-sky-400/10 border border-sky-400/25 p-3 text-center">
                <p className="text-xs text-sky-300">{t.community.totalPoints}</p>
                <p className="text-lg font-extrabold text-white mt-0.5">{totalPoints}</p>
              </div>
              <div className="rounded-xl bg-slate-900 border border-slate-800 p-3 text-center">
                <p className="text-xs text-slate-400">{t.community.activitiesLogged}</p>
                <p className="text-lg font-extrabold text-white mt-0.5">{activities.length}</p>
              </div>
            </div>

            <form onSubmit={handleActivitySubmit} className="space-y-3.5 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.activityTypeLabel}
                </label>
                <select
                  value={activityForm.activity_type}
                  onChange={(e) =>
                    setActivityForm({ ...activityForm, activity_type: e.target.value })
                  }
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                >
                  {Object.keys(t.community.activityTypes).map((key) => (
                    <option key={key} value={key}>
                      {t.community.activityTypes[key]}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  {t.community.activityDescLabel}
                </label>
                <input
                  type="text"
                  required
                  minLength={4}
                  value={activityForm.description}
                  onChange={(e) =>
                    setActivityForm({ ...activityForm, description: e.target.value })
                  }
                  placeholder={t.community.activityDescPlaceholder}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white focus:outline-none focus:border-emerald-400"
                />
              </div>

              <button
                type="submit"
                disabled={submittingActivity}
                className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm transition cursor-pointer disabled:opacity-50"
              >
                {submittingActivity ? t.common.saving : t.community.logActivityBtn}
              </button>
            </form>
          </div>

          <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-3">
            {activities.length === 0 ? (
              <p className="text-sm text-slate-400">{t.community.noActivities}</p>
            ) : (
              <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                {activities.map((act) => (
                  <div
                    key={act.id}
                    className="rounded-xl bg-slate-900/85 border border-slate-800 p-3.5 flex items-center justify-between gap-3"
                  >
                    <div>
                      <p className="text-sm font-semibold text-emerald-300">
                        {t.community.activityTypes[act.activity_type] || act.activity_type}
                      </p>
                      <p className="text-xs text-slate-300 mt-0.5">{act.description}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <span className="inline-block px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 text-xs font-bold">
                        -{act.co2_saved_kg} kg CO2
                      </span>
                      <p className="text-[11px] text-sky-300 mt-1">+{act.points} pts</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
