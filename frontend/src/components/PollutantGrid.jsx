import { useLanguage } from '../hooks/useLanguage';

export function PollutantGrid({ pollutants }) {
  const { t } = useLanguage();
  if (!pollutants) return null;

  const cards = [
    { key: 'pm25', value: pollutants.pm25, unit: 'µg/m³', maxRef: 150 },
    { key: 'pm10', value: pollutants.pm10, unit: 'µg/m³', maxRef: 250 },
    { key: 'co', value: pollutants.co, unit: 'µg/m³', maxRef: 4000 },
    { key: 'no2', value: pollutants.no2, unit: 'µg/m³', maxRef: 200 },
    { key: 'so2', value: pollutants.so2, unit: 'µg/m³', maxRef: 150 },
    { key: 'o3', value: pollutants.o3, unit: 'µg/m³', maxRef: 180 },
  ];

  return (
    <section className="space-y-3">
      <h3 className="text-base sm:text-lg font-bold text-white">{t.dashboard.pollutantsHeading}</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {cards.map((item) => {
          const info = t.dashboard.pollutantInfo[item.key];
          const ratio = Math.min(100, Math.max(6, Math.round((item.value / item.maxRef) * 100)));
          const barColor =
            ratio > 70 ? 'bg-amber-400' : ratio > 40 ? 'bg-sky-400' : 'bg-emerald-400';

          return (
            <div
              key={item.key}
              className="glass-panel rounded-2xl p-4 sm:p-5 hover:border-emerald-400/40 transition-colors duration-200 flex flex-col justify-between gap-3"
            >
              <div className="flex items-baseline justify-between gap-2">
                <span className="text-sm font-bold text-emerald-300 tracking-wide">
                  {info.name}
                </span>
                <span className="text-xl font-extrabold text-white">
                  {item.value}{' '}
                  <span className="text-xs font-medium text-slate-400">{item.unit}</span>
                </span>
              </div>

              <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className={`h-full rounded-full ${barColor} transition-all duration-500`}
                  style={{ width: `${ratio}%` }}
                />
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{info.desc}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
