import { useState } from 'react';
import { Info, RefreshCw, Search } from 'lucide-react';
import { AqiGaugeCard } from '../components/AqiGaugeCard';
import { PollutantGrid } from '../components/PollutantGrid';
import { PrecautionsPanel } from '../components/PrecautionsPanel';
import { RoutineUpdatesPanel } from '../components/RoutineUpdatesPanel';
import { TrendChartCard } from '../components/TrendChartCard';
import { WeatherCard } from '../components/WeatherCard';
import { useLanguage } from '../hooks/useLanguage';

export function DashboardPage({ data, loading, error, cityQuery, onChangeCity, onRefresh }) {
  const { t } = useLanguage();
  const [searchInput, setSearchInput] = useState(cityQuery || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      onChangeCity(searchInput.trim());
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & City Search */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {t.dashboard.title}
          </h2>
          <p className="text-sm text-sky-200/80 mt-1">{t.dashboard.subtitle}</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-wrap sm:flex-nowrap items-center gap-2">
          <div className="relative flex-1 sm:w-72">
            <Search className="h-4 w-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder={t.common.searchCityPlaceholder}
              className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-sky-400/25 text-sm text-white placeholder:text-slate-400 focus:outline-none focus:border-emerald-400"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm transition cursor-pointer"
          >
            {t.common.searchBtn}
          </button>
          <button
            type="button"
            onClick={onRefresh}
            disabled={loading}
            className="p-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-sky-400/20 text-sky-200 transition cursor-pointer disabled:opacity-50"
            title={t.common.refresh}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </form>
      </div>

      {/* Quick City Switchers */}
      <div className="flex flex-wrap items-center gap-2">
        {t.dashboard.quickCities.map((city) => (
          <button
            key={city}
            type="button"
            onClick={() => {
              setSearchInput(city);
              onChangeCity(city);
            }}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition cursor-pointer ${
              data?.location?.toLowerCase().includes(city.toLowerCase())
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/40'
                : 'bg-slate-900/70 text-slate-300 border-slate-700/80 hover:border-sky-400/40'
            }`}
          >
            {city}
          </button>
        ))}
      </div>

      {/* Error State */}
      {error && (
        <div className="rounded-xl bg-red-500/15 border border-red-400/40 px-4 py-3 text-sm text-red-200">
          {t.common.errorPrefix}: {error}
        </div>
      )}

      {/* Demonstration Data Banner (if live API unavailable) */}
      {data?.notice && (
        <div className="rounded-xl bg-sky-400/12 border border-sky-400/35 px-4 py-3 flex items-start gap-2.5 text-xs sm:text-sm text-sky-100">
          <Info className="h-4 w-4 text-sky-300 shrink-0 mt-0.5" />
          <span>{data.notice}</span>
        </div>
      )}

      {loading && !data ? (
        <div className="glass-panel rounded-2xl p-10 text-center text-sky-200">
          {t.common.loading}
        </div>
      ) : data ? (
        <>
          {/* Top Summary Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <div className="lg:col-span-2">
              <AqiGaugeCard data={data} />
            </div>
            <div>
              <WeatherCard weather={data.weather} />
            </div>
          </div>

          {/* Interactive Hourly Chart */}
          <TrendChartCard hourlyTrend={data.hourly_trend} />

          {/* Pollutant Cards */}
          <PollutantGrid pollutants={data.pollutants} />

          {/* Precautions & Personalized Daily Routine */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <PrecautionsPanel precautions={data.precautions} />
            <RoutineUpdatesPanel
              dailyUpdates={data.daily_updates}
              personalizedRoutine={data.personalized_routine}
            />
          </div>
        </>
      ) : null}
    </div>
  );
}
