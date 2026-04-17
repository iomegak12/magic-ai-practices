import { Routes, Route, Navigate } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import LibraryPage from './pages/LibraryPage';
import SettingsPage from './pages/SettingsPage';

function BackgroundBlobs() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <div
        style={{
          position: 'absolute',
          top: '-10%',
          left: '-10%',
          width: '45vw',
          height: '45vw',
          borderRadius: '50%',
          background: 'rgba(180, 140, 240, 0.35)',
          filter: 'blur(70px)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: '-10%',
          right: '-5%',
          width: '40vw',
          height: '40vw',
          borderRadius: '50%',
          background: 'rgba(140, 180, 255, 0.30)',
          filter: 'blur(70px)',
        }}
      />
    </div>
  );
}

export default function App() {
  return (
    <>
      <BackgroundBlobs />
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/chat/:sessionId" element={<ChatPage />} />
        <Route path="/library" element={<LibraryPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}
