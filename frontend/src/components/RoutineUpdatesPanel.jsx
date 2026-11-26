import { CalendarCheck2, Sparkles } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';

export function RoutineUpdatesPanel({ dailyUpdates, personalizedRoutine }) {
  const { t } = useLanguage();

  return (
    <div className="space-y-4">
      <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-sky-300" />
          <h3 className="text-base sm:text-lg font-bold text-white">{t.dashboard.updatesHeading}</h3>
        </div>
        <div className="space-y-2.5">
          {(dailyUpdates || []).map((item, idx) => (
            <div
              key={`${item.title}-${idx}`}
              className="rounded-xl bg-slate-900/75 border border-slate-800 p-3.5"
            >
              <h4 className="text-sm font-semibold text-sky-200">{item.title}</h4>
              <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">{item.detail}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center gap-2">
          <CalendarCheck2 className="h-5 w-5 text-emerald-400" />
          <h3 className="text-base sm:text-lg font-bold text-white">{t.dashboard.routineHeading}</h3>
        </div>
        <div className="space-y-2.5">
          {(personalizedRoutine || []).map((item, idx) => (
            <div
              key={`${item.title}-${idx}`}
              className="rounded-xl bg-emerald-500/8 border border-emerald-400/20 p-3.5"
            >
              <h4 className="text-sm font-semibold text-emerald-300">{item.title}</h4>
              <p className="text-xs sm:text-sm text-slate-200 mt-1 leading-relaxed">{item.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
