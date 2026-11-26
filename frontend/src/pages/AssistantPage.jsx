import { useEffect, useRef, useState } from 'react';
import {
  AlertCircle,
  Bot,
  KeyRound,
  Send,
  ShieldAlert,
  Sparkles,
  Trash2,
  User,
} from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';
import { api } from '../services/api';

export function AssistantPage({ sessionId, dashboardData, aiConfigured }) {
  const { language, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [error, setError] = useState(null);
  const [setupGuide, setSetupGuide] = useState(null);
  const scrollEndRef = useRef(null);

  useEffect(() => {
    let active = true;
    api
      .getChatHistory(sessionId)
      .then((res) => {
        if (active) setMessages(res.messages || []);
      })
      .catch(() => {
        // ignore initial history load errors gracefully
      });
    return () => {
      active = false;
    };
  }, [sessionId]);

  useEffect(() => {
    scrollEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending, setupGuide]);

  const sendMessage = async (textOverride) => {
    const content = (textOverride ?? input).trim();
    if (!content || sending) return;

    setError(null);
    setSetupGuide(null);
    if (!textOverride) setInput('');

    const optimisticUser = {
      id: Date.now(),
      role: 'user',
      content,
      language,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimisticUser]);
    setSending(true);

    try {
      const res = await api.sendChat({
        message: content,
        language,
        session_id: sessionId,
        city: dashboardData?.location,
        include_aqi_context: true,
      });

      if (!res.configured) {
        setSetupGuide(res.setup_guide);
        return;
      }

      if (res.error) {
        setError(res.error);
        return;
      }

      if (res.reply) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: 'assistant',
            content: res.reply,
            language: res.language,
            model_used: res.model_used,
            created_at: res.created_at,
          },
        ]);
      }
    } catch (err) {
      setError(err.message || 'Failed to reach AI assistant endpoint.');
    } finally {
      setSending(false);
    }
  };

  const handleClear = async () => {
    setClearing(true);
    setError(null);
    setSetupGuide(null);
    try {
      await api.clearChatHistory(sessionId);
      setMessages([]);
    } catch (err) {
      setError(err.message);
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {t.assistant.title}
          </h2>
          <p className="text-sm text-sky-200/80 mt-1">{t.assistant.subtitle}</p>
        </div>

        <button
          type="button"
          onClick={handleClear}
          disabled={clearing || messages.length === 0}
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition cursor-pointer disabled:opacity-40 self-start sm:self-auto"
        >
          <Trash2 className="h-3.5 w-3.5 text-rose-400" />
          {clearing ? t.assistant.clearing : t.assistant.clearChat}
        </button>
      </div>

      {/* Safety Policy Banner */}
      <div className="rounded-xl bg-amber-500/10 border border-amber-400/30 px-4 py-3 flex items-start gap-2.5 text-xs sm:text-sm text-amber-100">
        <ShieldAlert className="h-4 w-4 text-amber-300 shrink-0 mt-0.5" />
        <span>{t.assistant.safetyBanner}</span>
      </div>

      {/* Suggested Questions */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="inline-flex items-center gap-1.5 font-semibold text-emerald-300">
            <Sparkles className="h-3.5 w-3.5" />
            {t.assistant.suggestedTitle}
          </span>
          {dashboardData && (
            <span className="text-sky-300">
              {t.assistant.contextActive} ({dashboardData.location}: AQI {dashboardData.pollutants?.aqi})
            </span>
          )}
        </div>
        <div className="flex flex-wrap gap-2">
          {t.assistant.suggestedQuestions.map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => sendMessage(q)}
              disabled={sending}
              className="text-left px-3 py-2 rounded-xl bg-slate-900/90 hover:bg-emerald-500/15 border border-sky-400/20 hover:border-emerald-400/40 text-xs text-slate-200 transition cursor-pointer"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* AI Key Status Notice (visible immediately if AI_API_KEY is not set) */}
      {aiConfigured === false && (
        <div className="rounded-xl bg-sky-400/12 border border-sky-400/35 px-4 py-3 flex items-start gap-2.5 text-xs sm:text-sm text-sky-100">
          <KeyRound className="h-4 w-4 text-sky-300 shrink-0 mt-0.5" />
          <div>
            <strong className="block text-white">{t.assistant.setupMissingTitle}</strong>
            <span>{t.assistant.setupMissingInline}</span>
          </div>
        </div>
      )}

      {/* Error Alert */}
      {error && (
        <div className="rounded-xl bg-red-500/15 border border-red-400/40 px-4 py-3 flex items-start gap-2.5 text-sm text-red-200">
          <AlertCircle className="h-4 w-4 text-red-300 shrink-0 mt-0.5" />
          <span>
            {t.common.errorPrefix}: {error}
          </span>
        </div>
      )}

      {/* Chat Thread */}
      <div className="glass-panel rounded-2xl flex flex-col h-[460px] sm:h-[520px] overflow-hidden">
        <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
          {messages.length === 0 && !sending && !setupGuide ? (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto space-y-3">
              <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-emerald-400/20 to-sky-400/20 border border-emerald-400/30 flex items-center justify-center">
                <Bot className="h-7 w-7 text-emerald-400" />
              </div>
              <h3 className="text-lg font-bold text-white">{t.assistant.emptyStateTitle}</h3>
              <p className="text-sm text-slate-300 leading-relaxed">{t.assistant.emptyStateDesc}</p>
            </div>
          ) : (
            messages.map((msg) => {
              const isUser = msg.role === 'user';
              return (
                <div
                  key={msg.id}
                  className={`flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
                >
                  {!isUser && (
                    <div className="h-8 w-8 rounded-xl bg-emerald-500/20 border border-emerald-400/35 flex items-center justify-center shrink-0">
                      <Bot className="h-4 w-4 text-emerald-300" />
                    </div>
                  )}
                  <div
                    className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                      isUser
                        ? 'bg-gradient-to-r from-emerald-500 to-sky-400 text-slate-950 font-medium'
                        : 'bg-slate-900/90 border border-slate-700/80 text-slate-100'
                    }`}
                  >
                    {msg.content}
                    {msg.model_used && (
                      <div className="mt-2 pt-1.5 border-t border-slate-800 text-[10px] text-slate-400">
                        {msg.model_used}
                      </div>
                    )}
                  </div>
                  {isUser && (
                    <div className="h-8 w-8 rounded-xl bg-sky-400/20 border border-sky-400/35 flex items-center justify-center shrink-0">
                      <User className="h-4 w-4 text-sky-300" />
                    </div>
                  )}
                </div>
              );
            })
          )}

          {/* Setup Guide rendered directly inside the chat thread when AI_API_KEY is missing */}
          {setupGuide && (
            <div className="rounded-2xl bg-slate-900/95 border border-sky-400/40 p-4 sm:p-5 space-y-3">
              <div className="flex items-center gap-2.5 text-sky-300">
                <KeyRound className="h-5 w-5 shrink-0" />
                <h3 className="text-base font-bold text-white">{setupGuide.title}</h3>
              </div>
              <p className="text-sm text-slate-200 leading-relaxed">{setupGuide.explanation}</p>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-emerald-300 mb-1.5">
                  {t.assistant.setupStepsTitle}
                </p>
                <ol className="list-decimal list-inside space-y-1 text-xs sm:text-sm text-slate-300">
                  {setupGuide.steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
              <pre className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs text-emerald-300 overflow-x-auto">
                {setupGuide.env_example}
              </pre>
            </div>
          )}

          {sending && (
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-xl bg-emerald-500/20 border border-emerald-400/35 flex items-center justify-center">
                <Bot className="h-4 w-4 text-emerald-300 animate-pulse" />
              </div>
              <div className="rounded-2xl px-4 py-2.5 bg-slate-900/90 border border-slate-800 text-xs sm:text-sm text-sky-200">
                {t.assistant.typing}
              </div>
            </div>
          )}
          <div ref={scrollEndRef} />
        </div>

        {/* Input Composer */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
          className="p-3 sm:p-4 border-t border-sky-400/15 bg-slate-950/80 flex items-center gap-2.5"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.assistant.inputPlaceholder}
            disabled={sending}
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-sky-400/25 text-sm text-white placeholder:text-slate-400 focus:outline-none focus:border-emerald-400"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm transition cursor-pointer disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
            <span className="hidden sm:inline">{t.assistant.send}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
