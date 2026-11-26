import { useCallback, useEffect, useState } from 'react';
import { LanguageProvider, useLanguage } from './hooks/useLanguage';
import { useSessionId } from './hooks/useSessionId';
import { MainLayout } from './layouts/MainLayout';
import { AssistantPage } from './pages/AssistantPage';
import { CommunityPage } from './pages/CommunityPage';
import { DashboardPage } from './pages/DashboardPage';
import { PreferencesPage } from './pages/PreferencesPage';
import { api } from './services/api';

function AppShell() {
  const { language } = useLanguage();
  const sessionId = useSessionId();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [cityQuery, setCityQuery] = useState('');
  const [dashboardData, setDashboardData] = useState(null);
  const [loadingDashboard, setLoadingDashboard] = useState(true);
  const [dashboardError, setDashboardError] = useState('');
  const [healthStatus, setHealthStatus] = useState(null);

  const loadHealth = useCallback(async () => {
    try {
      const res = await api.getHealth();
      setHealthStatus(res);
    } catch {
      setHealthStatus({ status: 'offline' });
    }
  }, []);

  const loadDashboard = useCallback(
    async (overrideCity) => {
      setLoadingDashboard(true);
      setDashboardError('');
      try {
        const res = await api.getDashboard({
          city: overrideCity !== undefined ? overrideCity : cityQuery,
          lang: language,
          sessionId,
        });
        setDashboardData(res);
      } catch (err) {
        setDashboardError(err.message || 'Unable to load dashboard data.');
      } finally {
        setLoadingDashboard(false);
      }
    },
    [cityQuery, language, sessionId]
  );

  useEffect(() => {
    loadHealth();
  }, [loadHealth]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const handleChangeCity = (nextCity) => {
    setCityQuery(nextCity);
    loadDashboard(nextCity);
  };

  const handlePreferencesSaved = (savedPrefs) => {
    setCityQuery(savedPrefs.location);
    loadDashboard(savedPrefs.location);
  };

  return (
    <MainLayout
      activeTab={activeTab}
      onSelectTab={setActiveTab}
      healthStatus={healthStatus}
      currentCity={dashboardData?.location}
      isLive={Boolean(dashboardData?.is_live)}
    >
      {activeTab === 'dashboard' && (
        <DashboardPage
          data={dashboardData}
          loading={loadingDashboard}
          error={dashboardError}
          cityQuery={cityQuery}
          onChangeCity={handleChangeCity}
          onRefresh={() => loadDashboard()}
        />
      )}
      {activeTab === 'assistant' && (
        <AssistantPage
          sessionId={sessionId}
          dashboardData={dashboardData}
          aiConfigured={healthStatus?.ai_configured}
        />
      )}
      {activeTab === 'preferences' && (
        <PreferencesPage sessionId={sessionId} onPreferencesSaved={handlePreferencesSaved} />
      )}
      {activeTab === 'community' && <CommunityPage sessionId={sessionId} />}
    </MainLayout>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppShell />
    </LanguageProvider>
  );
}
