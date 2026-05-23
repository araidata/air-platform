export const labelize = (value: string | null | undefined) =>
  (value ?? "unknown")
    .split("_")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

export const formatDate = (value: string | null | undefined) => {
  if (!value) return "Not set";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(value));
};

export const statusTone = (status: string) => {
  if (["approved", "completed", "closed", "mitigated", "passed"].includes(status)) {
    return "border-emerald-300/20 bg-emerald-300/10 text-emerald-100";
  }
  if (["blocked", "failed", "critical", "high"].includes(status)) {
    return "border-red-300/20 bg-red-300/10 text-red-100";
  }
  if (
    [
      "pending",
      "under_review",
      "awaiting_retest",
      "risk_accepted",
      "approved_with_exception",
      "medium",
    ].includes(status)
  ) {
    return "border-amber-300/20 bg-amber-300/10 text-amber-100";
  }
  if (["running", "in_remediation"].includes(status)) {
    return "border-cyan-300/20 bg-cyan-300/10 text-cyan-100";
  }
  return "border-white/10 bg-white/[0.06] text-zinc-300";
};

export function StatusPill({ value }: { value: string }) {
  return (
    <span className={`inline-flex rounded-md border px-2 py-1 text-xs ${statusTone(value)}`}>
      {labelize(value)}
    </span>
  );
}
