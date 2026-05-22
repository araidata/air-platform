export function ScoreRing({
  score,
  label = "Risk score",
}: {
  score: number;
  label?: string;
}) {
  const color =
    score < 50 ? "#f87171" : score < 70 ? "#fbbf24" : score < 85 ? "#67e8f9" : "#6ee7b7";

  return (
    <div className="flex items-center gap-3">
      <div
        className="grid size-16 place-items-center rounded-full"
        style={{
          background: `conic-gradient(${color} ${score * 3.6}deg, rgba(255,255,255,0.08) 0deg)`,
        }}
        aria-label={`${label}: ${score}`}
      >
        <div className="grid size-[52px] place-items-center rounded-full bg-[#101418]">
          <span className="font-mono text-lg font-semibold text-zinc-100">
            {score}
          </span>
        </div>
      </div>
      <div>
        <p className="text-sm font-medium text-zinc-100">{label}</p>
        <p className="text-xs text-zinc-500">0 to 100 operating score</p>
      </div>
    </div>
  );
}
