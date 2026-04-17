import { useState, useEffect } from 'react';

const DISMISSED_KEY = 'clonescript_upgrade_dismissed';

export default function UpgradeCard() {
  const [dismissed, setDismissed] = useState(() => {
    return localStorage.getItem(DISMISSED_KEY) === 'true';
  });

  useEffect(() => {
    localStorage.setItem(DISMISSED_KEY, String(dismissed));
  }, [dismissed]);

  if (dismissed) return null;

  return (
    <div className="glass-card rounded-card p-4 mt-4 relative">
      <button
        onClick={() => setDismissed(true)}
        className="absolute top-2 right-2 text-text-muted hover:text-text-primary text-sm"
        aria-label="Dismiss"
      >
        ✕
      </button>

      {/* Orb avatar */}
      <div
        className="w-10 h-10 rounded-full mx-auto mb-3"
        style={{
          background: 'radial-gradient(circle at 35% 35%, #c084fc, #818cf8, #312e81)',
        }}
      />

      <h4 className="text-[15px] font-bold text-text-primary text-center">
        Upgrade to Pro
      </h4>
      <p className="text-[13px] text-text-secondary text-center mt-1 mb-3">
        Unlock unlimited conversations, priority access, and more.
      </p>
      <button className="w-full py-2 px-4 rounded-lg border border-text-primary text-text-primary text-[13px] font-medium hover:bg-gray-50 transition-colors">
        Upgrade Now
      </button>
    </div>
  );
}
