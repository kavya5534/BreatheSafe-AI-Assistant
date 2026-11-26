import { Clock, Database, Radio } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';

export function AqiGaugeCard({ data }) {
  const { t } = useLanguage();
  const aqi = data?.pollutants?.aqi ?? 0;
  const severity = data?.severity;
  const color = severity?.color_hex || '#10b981';

  // Gauge arc calculation (0-350 mapped to circumference)
  const clamped = Math.min(350, Math.max(0, aqi));
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const progress = (clamped / 350) * circumference;

  const formattedTime = (() => {
    try {
      return new Date(data.last_updated).toLocaleString();
    } catch {
      return data?.last_updated || '';
    }
  })();

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 flex flex-col justify-between gap-5 relative overflow-hidden">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-sky-300">
            {t.dashboard.currentAqi}
          </p>
          <h2 className="text-xl sm:text-2xl font-bold text-white mt-0.5">{data.location}</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            {t.common.coordinates}: {data.latitude?.toFixed(2)}, {data.longitude?.toFixed(2)}
          </p>
        </div>

        <span
          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${
            data.is_live
              ? 'bg-emerald-500/15 text-emerald-300 border-emerald-400/35'
              : 'bg-amber-500/15 text-amber-200 border-amber-400/35'
          }`}
        >
          <Radio className="h-3.5 w-3.5" />
          {data.is_live ? t.nav.liveStatus : t.nav.demoStatus}
        </span>
      </div>

      {/* Radial Gauge + Severity Summary */}
      <div className="flex flex-col sm:flex-row items-center gap-6">
        <div className="relative h-40 w-40 shrink-0 flex items-center justify-center">
          <svg className="h-40 w-40 -rotate-90" viewBox="0 0 160 160">
            <circle
              cx="80"
              cy="80"
              r={radius}
              fill="none"
              stroke="rgba(148, 163, 184, 0.18)"
              strokeWidth="12"
            />
            <circle
              cx="80"
              cy="80"
              r={radius}
              fill="none"
              stroke={color}
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={`${progress} ${circumference}`}
              className="transition-all duration-700 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-extrabold text-white tracking-tight">{aqi}</span>
            <span className="text-[11px] font-medium text-sky-200/80 mt-0.5">
              {t.dashboard.aqiScale}
            </span>
          </div>
        </div>

        <div className="flex-1 space-y-3 text-center sm:text-left">
          <div>
            <p className="text-xs uppercase tracking-wider text-slate-400">
              {t.dashboard.severityHeading}
            </p>
            <div className="mt-1 inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-900/90 border border-slate-700/70">
              <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: color }} />
              <span className="text-base font-bold text-white">{severity?.label}</span>
            </div>
          </div>
          <p className="text-sm text-slate-200 leading-relaxed">{severity?.summary}</p>
        </div>
      </div>

      {/* Source & Timestamp Footer */}
      <div className="pt-3 border-t border-slate-800/90 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-400">
        <span className="inline-flex items-center gap-1.5">
          <Database className="h-3.5 w-3.5 text-sky-400 shrink-0" />
          <span>
            {t.common.dataSource}: <strong className="text-slate-200">{data.data_source}</strong>
          </span>
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Clock className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
          <span>
            {t.common.lastUpdated}: <strong className="text-slate-200">{formattedTime}</strong>
          </span>
        </span>
      </div>
    </div>
  );
}
