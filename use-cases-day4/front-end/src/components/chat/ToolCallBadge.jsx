export default function ToolCallBadge({ tool }) {
  const name = typeof tool === 'string' ? tool : tool.name;
  const duration = typeof tool === 'object' ? tool.duration_seconds : null;

  return (
    <span className="inline-flex items-center gap-1 bg-white/80 border border-gray-200/55 rounded-full px-2.5 py-0.5 text-[11px] text-text-secondary">
      <span className="font-medium">{name}</span>
      {duration != null && (
        <span className="text-text-muted">{duration.toFixed(1)}s</span>
      )}
    </span>
  );
}
