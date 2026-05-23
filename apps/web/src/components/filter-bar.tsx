export function FilterBar({
  items,
  activeItem,
  onChange,
}: {
  items: string[];
  activeItem?: string;
  onChange?: (item: string) => void;
}) {
  return (
    <div className="mb-4 flex flex-wrap gap-2">
      {items.map((item, index) => {
        const active = activeItem ? activeItem === item : index === 0;
        const className = `rounded-md border px-3 py-1.5 text-xs font-medium ${
          active
              ? "border-cyan-300/25 bg-cyan-300/10 text-cyan-100"
              : "border-white/10 bg-white/[0.045] text-zinc-400"
        }`;

        if (onChange) {
          return (
            <button key={item} type="button" onClick={() => onChange(item)} className={className}>
              {item}
            </button>
          );
        }

        return (
          <span key={item} className={className}>
            {item}
          </span>
        );
      })}
    </div>
  );
}
