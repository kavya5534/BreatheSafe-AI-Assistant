import { createContext, useContext, useEffect, useState } from 'react';
import { translations } from '../translations';

const LANG_STORAGE_KEY = 'breathesafe_language';
const VALID_LANGUAGES = ['en', 'kn', 'hi'];

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    try {
      const saved = localStorage.getItem(LANG_STORAGE_KEY);
      return VALID_LANGUAGES.includes(saved) ? saved : 'en';
    } catch {
      return 'en';
    }
  });

  const setLanguage = (nextLang) => {
    const normalized = VALID_LANGUAGES.includes(nextLang) ? nextLang : 'en';
    setLanguageState(normalized);
    try {
      localStorage.setItem(LANG_STORAGE_KEY, normalized);
    } catch {
      // ignore storage errors
    }
  };

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const t = translations[language] || translations.en;

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return ctx;
}
