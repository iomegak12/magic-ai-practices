import Sidebar from '../components/layout/Sidebar';

export default function SettingsPage() {
  return (
    <div className="max-w-[1200px] mx-auto my-6 px-4 h-[calc(100vh-48px)] flex gap-4">
      <Sidebar />
      <main className="glass-panel rounded-panel flex-1 flex items-center justify-center p-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-text-primary mb-2">Settings</h2>
          <p className="text-text-secondary">Configuration options coming soon.</p>
        </div>
      </main>
    </div>
  );
}
