const ACTIONS = [
  { icon: '🖼️', label: 'Create Images' },
  { icon: '📖', label: 'Study' },
  { icon: '🔨', label: 'Build' },
  { icon: '🔍', label: 'Deep Research' },
  { icon: '📚', label: 'Learn' },
];

export default function ActionBar() {
  return (
    <div className="flex items-center justify-center gap-2 mt-3 flex-wrap">
      {ACTIONS.map(({ icon, label }) => (
        <button
          key={label}
          className="bg-white/80 border border-gray-200/55 rounded-full px-3.5 py-1.5 text-[13px] text-[var(--color-pill-text)] hover:shadow-md transition-shadow flex items-center gap-1.5"
        >
          <span className="text-sm">{icon}</span>
          {label}
        </button>
      ))}
    </div>
  );
}
