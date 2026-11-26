import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';

export function PrecautionsPanel({ precautions }) {
  const { t } = useLanguage();

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div className="flex items-center gap-2.5">
        <ShieldAlert className="h-5 w-5 text-emerald-400" />
        <h3 className="text-base sm:text-lg font-bold text-white">
          {t.dashboard.precautionsHeading}
        </h3>
      </div>

      <div className="space-y-3">
        {(precautions || []).map((item, idx) => (
          <div
            key={`${item.title}-${idx}`}
            className="rounded-xl bg-slate-900/80 border border-slate-800 p-4 space-y-2"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                <h4 className="text-sm font-bold text-white">{item.title}</h4>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-sky-400/15 text-sky-300 border border-sky-400/25">
                {item.audience}
              </span>
            </div>
            <p className="text-sm text-slate-200 leading-relaxed">{item.detail}</p>
            <p className="text-xs text-emerald-300/90 bg-emerald-500/10 border border-emerald-500/20 rounded-lg px-3 py-2">
              <strong>{t.common.whyUseful}:</strong> {item.reason}
            </p>
          </div>
        ))}
      </div>

      <div className="rounded-xl bg-amber-500/10 border border-amber-400/30 p-3.5 flex items-start gap-2.5 text-xs text-amber-100 leading-relaxed">
        <AlertTriangle className="h-4 w-4 text-amber-300 shrink-0 mt-0.5" />
        <div>
          <strong className="block text-amber-200">{t.dashboard.medicalBannerTitle}</strong>
          <span>{t.dashboard.medicalBannerText}</span>
        </div>
      </div>
    </div>
  );
}
