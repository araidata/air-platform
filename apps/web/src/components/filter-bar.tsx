export function FilterBar({ items }: { items: string[] }) {
  return (
    <div className="mb-4 flex flex-wrap gap-2">
      {items.map((item, index) => (
        <span
          key={item}
          className={`rounded-md border px-3 py-1.5 text-xs font-medium ${
            index === 0
              ? "border-cyan-300/25 bg-cyan-300/10 text-cyan-100"
              : "border-white/10 bg-white/[0.045] text-zinc-400"
          }`}
        >
          {item}
        </span>
      ))}
    </div>
  );
}
