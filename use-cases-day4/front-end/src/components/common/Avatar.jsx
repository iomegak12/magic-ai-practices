export default function Avatar() {
  return (
    <div className="glass-card rounded-xl px-3 py-2 flex items-center gap-2.5">
      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-400 to-indigo-500 flex items-center justify-center text-white text-sm font-semibold">
        U
      </div>
      <div className="hidden sm:block">
        <p className="text-[14px] font-semibold text-text-primary leading-tight">
          User
        </p>
        <p className="text-[12px] text-text-muted leading-tight">
          user@example.com
        </p>
      </div>
    </div>
  );
}
