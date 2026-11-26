import { useState } from 'react';
import {
  Activity,
  Bot,
  Globe,
  Menu,
  ShieldCheck,
  SlidersHorizontal,
  Users,
  Wind,
  X,
} from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';
import { LANGUAGE_OPTIONS } from '../translations';

export function MainLayout({
  activeTab,
  onSelectTab,
  healthStatus,
  currentCity,
  isLive,
  children,
}) {
  const { language, setLanguage, t } = useLanguage();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: t.nav.dashboard, icon: Activity },
    { id: 'assistant', label: t.nav.assistant, icon: Bot },
    { id: 'preferences', label: t.nav.preferences, icon: SlidersHorizontal },
    { id: 'community', label: t.nav.community, icon: Users },
  ];

  const handleNavClick = (tabId) => {
    onSelectTab(tabId);
    setMobileMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-[#060d1f] text-slate-100 flex flex-col lg:flex-row">
      {/* Ambient futuristic radial gradients */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 h-96 w-96 rounded-full bg-emerald-500/12 blur-3xl" />
        <div className="absolute top-1/3 -right-32 h-96 w-96 rounded-full bg-sky-400/10 blur-3xl" />
      </div>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:flex-col lg:w-72 lg:shrink-0 border-r border-sky-400/15 bg-[#09132b]/95 backdrop-blur-xl z-20">
        <div className="p-6 border-b border-sky-400/15">
          <div className="flex items-center gap-3">
            <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-emerald-400 to-sky-400 flex items-center justify-center shadow-lg shadow-emerald-500/25">
              <Wind className="h-6 w-6 text-slate-950" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">{t.brand.name}</h1>
              <p className="text-[11px] font-medium uppercase tracking-wider text-emerald-400">
                {t.brand.badge}
              </p>
            </div>
          </div>
          <p className="mt-3 text-xs text-sky-200/80 leading-relaxed">{t.brand.tagline}</p>
        </div>

        <nav className="flex-1 p-4 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = activeTab === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 cursor-pointer ${
                  active
                    ? 'bg-gradient-to-r from-emerald-500/20 to-sky-400/15 text-white border border-emerald-400/40 shadow-md shadow-emerald-950/50'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white border border-transparent'
                }`}
              >
                <Icon className={`h-5 w-5 ${active ? 'text-emerald-400' : 'text-sky-300/70'}`} />
                <span className="truncate">{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="p-4 m-4 rounded-2xl bg-slate-900/80 border border-sky-400/15 space-y-2.5">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400">{t.common.dataSource}</span>
            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full font-medium ${
                isLive
                  ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-400/30'
                  : 'bg-sky-400/15 text-sky-300 border border-sky-400/30'
              }`}
            >
              <span
                className={`h-1.5 w-1.5 rounded-full ${
                  isLive ? 'bg-emerald-400 animate-pulse' : 'bg-sky-400'
                }`}
              />
              {isLive ? t.nav.liveStatus : t.nav.demoStatus}
            </span>
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400">Backend</span>
            <span
              className={`inline-flex items-center gap-1 font-medium ${
                healthStatus?.status === 'ok' ? 'text-emerald-300' : 'text-amber-300'
              }`}
            >
              <ShieldCheck className="h-3.5 w-3.5" />
              {healthStatus?.status === 'ok' ? t.nav.backendOnline : t.nav.backendOffline}
            </span>
          </div>
          {currentCity && (
            <div className="pt-1 border-t border-slate-800 text-xs text-slate-300 truncate">
              📍 {currentCity}
            </div>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 z-10">
        {/* Top Navbar */}
        <header className="sticky top-0 z-30 border-b border-sky-400/15 bg-[#071026]/90 backdrop-blur-xl px-4 sm:px-6 py-3">
          <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
            {/* Mobile Brand + Menu Toggle */}
            <div className="flex items-center gap-3 lg:hidden">
              <button
                type="button"
                aria-label="Toggle navigation menu"
                onClick={() => setMobileMenuOpen((prev) => !prev)}
                className="p-2 rounded-xl bg-slate-800/80 border border-sky-400/20 text-slate-200 hover:text-white"
              >
                {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-emerald-400 to-sky-400 flex items-center justify-center">
                  <Wind className="h-4 w-4 text-slate-950" />
                </div>
                <span className="font-bold text-white text-sm sm:text-base">{t.brand.name}</span>
              </div>
            </div>

            {/* Desktop Page Breadcrumb */}
            <div className="hidden lg:flex items-center gap-3">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-400/25 text-emerald-300 text-xs font-semibold">
                {navItems.find((n) => n.id === activeTab)?.label}
              </span>
              {currentCity && (
                <span className="text-xs text-sky-200/80 font-medium">📍 {currentCity}</span>
              )}
            </div>

            {/* Language Selector in Navbar */}
            <div className="flex items-center gap-2 sm:gap-3 ml-auto">
              <div className="flex items-center gap-2 px-2.5 py-1.5 rounded-xl bg-slate-900/90 border border-sky-400/25">
                <Globe className="h-4 w-4 text-sky-300 shrink-0" />
                <label htmlFor="navbar-lang-select" className="sr-only">
                  {t.nav.languageLabel}
                </label>
                <select
                  id="navbar-lang-select"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-transparent text-xs sm:text-sm font-medium text-white focus:outline-none cursor-pointer pr-1"
                >
                  {LANGUAGE_OPTIONS.map((opt) => (
                    <option key={opt.code} value={opt.code} className="bg-slate-900 text-white">
                      {opt.nativeLabel} ({opt.label})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Mobile Drawer Menu */}
          {mobileMenuOpen && (
            <div className="lg:hidden mt-3 pt-3 border-t border-sky-400/15 space-y-1.5">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => handleNavClick(item.id)}
                    className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition ${
                      active
                        ? 'bg-emerald-500/20 text-white border border-emerald-400/40'
                        : 'text-slate-300 hover:bg-slate-800/70'
                    }`}
                  >
                    <Icon className={`h-4 w-4 ${active ? 'text-emerald-400' : 'text-sky-300'}`} />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          )}
        </header>

        {/* Page Body */}
        <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6 pb-24 lg:pb-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>

      {/* Mobile Bottom Navigation */}
      <nav className="lg:hidden fixed bottom-0 inset-x-0 z-30 bg-[#081229]/95 backdrop-blur-xl border-t border-sky-400/20 px-2 py-1.5 flex justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = activeTab === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => handleNavClick(item.id)}
              className={`flex flex-col items-center gap-0.5 px-2.5 py-1.5 rounded-xl text-[11px] font-medium transition ${
                active ? 'text-emerald-400 bg-emerald-500/10' : 'text-slate-400'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span className="max-w-[74px] truncate">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
