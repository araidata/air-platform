type MetricCardProps = {
  label: string;
  value: string | number;
  detail: string;
  tone?: "neutral" | "good" | "warn" | "bad";
};

const toneClasses = {
  neutral: "text-cyan-100",
  good: "text-emerald-100",
  warn: "text-amber-100",
  bad: "text-red-100",
};

export function MetricCard({
  label,
  value,
  detail,
  tone = "neutral",
}: MetricCardProps) {
  return (
    <section className="rounded-lg border border-white/10 bg-white/[0.055] p-4 shadow-[0_14px_40px_rgba(0,0,0,0.18)]">
      <p className="text-xs font-medium uppercase tracking-[0.08em] text-zinc-500">
        {label}
      </p>
      <div className="mt-3 flex items-end justify-between gap-3">
        <p className={`text-3xl font-semibold leading-none ${toneClasses[tone]}`}>
          {value}
        </p>
        <span className="rounded-md border border-white/10 bg-black/20 px-2 py-1 font-mono text-[11px] text-zinc-400">
          Phase 1
        </span>
      </div>
      <p className="mt-3 text-sm leading-5 text-zinc-400">{detail}</p>
    </section>
  );
}
