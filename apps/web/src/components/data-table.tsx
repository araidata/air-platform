export function TableShell({
  children,
  label,
}: {
  children: React.ReactNode;
  label: string;
}) {
  return (
    <div className="overflow-hidden rounded-lg border border-white/10 bg-white/[0.045]">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm" aria-label={label}>
          {children}
        </table>
      </div>
    </div>
  );
}

export function TableHead({ children }: { children: React.ReactNode }) {
  return (
    <thead className="border-b border-white/10 bg-black/20 text-xs uppercase tracking-[0.08em] text-zinc-500">
      {children}
    </thead>
  );
}

export function Th({ children }: { children: React.ReactNode }) {
  return <th className="px-4 py-3 font-semibold">{children}</th>;
}

export function Td({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <td className={`px-4 py-3 align-top ${className}`}>{children}</td>;
}
