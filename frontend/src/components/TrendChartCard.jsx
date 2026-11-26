import { useState } from 'react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { useLanguage } from '../hooks/useLanguage';

export function TrendChartCard({ hourlyTrend }) {
  const { t } = useLanguage();
  const [metric, setMetric] = useState('aqi');

  const metricOptions = [
    { key: 'aqi', label: t.dashboard.chartMetrics.aqi, color: '#10b981' },
    { key: 'pm25', label: t.dashboard.chartMetrics.pm25, color: '#38bdf8' },
    { key: 'pm10', label: t.dashboard.chartMetrics.pm10, color: '#a78bfa' },
    { key: 'o3', label: t.dashboard.chartMetrics.o3, color: '#f59e0b' },
  ];

  const activeMetric = metricOptions.find((m) => m.key === metric) || metricOptions[0];

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <h3 className="text-base sm:text-lg font-bold text-white">{t.dashboard.trendHeading}</h3>
        <div className="flex flex-wrap gap-1.5">
          {metricOptions.map((opt) => (
            <button
              key={opt.key}
              type="button"
              onClick={() => setMetric(opt.key)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                metric === opt.key
                  ? 'bg-emerald-500 text-slate-950 shadow-sm'
                  : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={hourlyTrend || []} margin={{ top: 10, right: 12, left: -16, bottom: 0 }}>
            <defs>
              <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={activeMetric.color} stopOpacity={0.45} />
                <stop offset="95%" stopColor={activeMetric.color} stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.14)" />
            <XAxis dataKey="time" stroke="#94a3b8" fontSize={11} />
            <YAxis stroke="#94a3b8" fontSize={11} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: 'rgba(56,189,248,0.35)',
                borderRadius: '12px',
                color: '#f8fafc',
                fontSize: '12px',
              }}
            />
            <Area
              type="monotone"
              dataKey={activeMetric.key}
              name={activeMetric.label}
              stroke={activeMetric.color}
              strokeWidth={2.5}
              fillOpacity={1}
              fill="url(#trendFill)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
