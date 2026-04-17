import { useNavigate, useLocation } from 'react-router-dom';

export default function NavItem({ icon, label, to, onClick }) {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = to && location.pathname === to;

  function handleClick() {
    if (onClick) {
      onClick();
    } else if (to) {
      navigate(to);
    }
  }

  return (
    <button
      onClick={handleClick}
      className={`flex items-center gap-2.5 px-2 py-2.5 text-[15px] rounded-lg w-full text-left transition-colors
        ${isActive
          ? 'text-[var(--color-text-link)] bg-white/40'
          : 'text-text-secondary hover:bg-white/40 hover:text-text-primary'
        }`}
    >
      <span className="w-5 text-center text-base">{icon}</span>
      <span>{label}</span>
    </button>
  );
}
