import ExampleCard from './ExampleCard';

const EXAMPLES = [
  { text: 'Write a to-do list for a personal project', icon: '👤' },
  { text: 'Generate an email to reply to a job offer', icon: '✉️' },
  { text: 'Summarize this article in one paragraph', icon: '💬' },
  { text: 'How does AI work in a technical capacity', icon: '💻' },
];

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good Morning';
  if (hour < 17) return 'Good Afternoon';
  return 'Good Evening';
}

export default function WelcomeScreen() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4">
      {/* Orb */}
      <div
        className="w-20 h-20 rounded-full mb-6"
        style={{
          background: 'radial-gradient(circle at 35% 35%, #c084fc, #818cf8, #312e81)',
        }}
      />

      {/* Greeting */}
      <h2 className="text-[36px] font-normal text-text-primary leading-tight mb-2">
        {getGreeting()},
        <br />
        how can I help you?
      </h2>
      <p className="text-[14px] text-text-secondary max-w-[480px] mx-auto mb-8">
        I can help you with writing, analysis, coding, math, and much more.
      </p>

      {/* Section label */}
      <p className="text-[11px] uppercase tracking-widest text-text-muted mb-3">
        Begin with the example below
      </p>

      {/* Example cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 w-full max-w-[640px]">
        {EXAMPLES.map((ex) => (
          <ExampleCard key={ex.text} text={ex.text} icon={ex.icon} />
        ))}
      </div>
    </div>
  );
}
