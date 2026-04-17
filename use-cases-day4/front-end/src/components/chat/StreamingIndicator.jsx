import LoadingDots from '../common/LoadingDots';

export default function StreamingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="glass-card rounded-card px-4 py-3">
        <LoadingDots />
      </div>
    </div>
  );
}
