import { CloudSun, Droplets, Thermometer, Wind } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';

export function WeatherCard({ weather }) {
  const { t } = useLanguage();
  if (!weather) return null;

  const stats = [
    {
      label: t.dashboard.temperature,
      value: `${weather.temperature_c}°C`,
      icon: Thermometer,
      accent: 'text-emerald-400',
    },
    {
      label: t.dashboard.feelsLike,
      value: `${weather.apparent_temp_c ?? weather.temperature_c}°C`,
      icon: CloudSun,
      accent: 'text-sky-300',
    },
    {
      label: t.dashboard.humidity,
      value: `${weather.humidity_pct}%`,
      icon: Droplets,
      accent: 'text-sky-400',
    },
    {
      label: t.dashboard.windSpeed,
      value: `${weather.wind_speed_kmh} km/h`,
      icon: Wind,
      accent: 'text-emerald-300',
    },
  ];

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 flex flex-col justify-between gap-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-sky-300">
            {t.dashboard.weatherHeading}
          </p>
          <h3 className="text-lg font-bold text-white mt-0.5">{weather.condition}</h3>
        </div>
        <div className="h-11 w-11 rounded-xl bg-sky-400/15 border border-sky-400/30 flex items-center justify-center">
          <CloudSun className="h-6 w-6 text-sky-300" />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.label}
              className="rounded-xl bg-slate-900/80 border border-slate-800 p-3.5 flex flex-col gap-1"
            >
              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <Icon className={`h-3.5 w-3.5 ${item.accent}`} />
                <span className="truncate">{item.label}</span>
              </div>
              <span className="text-lg font-bold text-white">{item.value}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
