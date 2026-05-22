import type {
  ApprovalStatus,
  AssessmentStatus,
  EvidenceRecord,
  FindingSeverity,
  FindingStatus,
  ReviewStatus,
  RiskTier,
} from "@/lib/mock-data";

type BadgeTone = "red" | "amber" | "green" | "blue" | "slate" | "violet";

const toneClasses: Record<BadgeTone, string> = {
  red: "border-red-400/25 bg-red-500/12 text-red-200",
  amber: "border-amber-300/25 bg-amber-400/12 text-amber-100",
  green: "border-emerald-300/25 bg-emerald-400/12 text-emerald-100",
  blue: "border-cyan-300/25 bg-cyan-400/12 text-cyan-100",
  slate: "border-white/12 bg-white/[0.06] text-zinc-200",
  violet: "border-violet-300/25 bg-violet-400/12 text-violet-100",
};

function Badge({ children, tone }: { children: React.ReactNode; tone: BadgeTone }) {
  return (
    <span
      className={`inline-flex min-h-6 items-center rounded-md border px-2 py-0.5 text-xs font-medium leading-tight ${toneClasses[tone]}`}
    >
      {children}
    </span>
  );
}

export function SeverityBadge({ severity }: { severity: FindingSeverity }) {
  const tone: Record<FindingSeverity, BadgeTone> = {
    Critical: "red",
    High: "amber",
    Medium: "blue",
    Low: "green",
  };

  return <Badge tone={tone[severity]}>{severity}</Badge>;
}

export function RiskTierBadge({ riskTier }: { riskTier: RiskTier }) {
  const tone: Record<RiskTier, BadgeTone> = {
    Critical: "red",
    High: "amber",
    Medium: "blue",
    Low: "green",
  };

  return <Badge tone={tone[riskTier]}>{riskTier}</Badge>;
}

export function ApprovalBadge({ status }: { status: ApprovalStatus }) {
  const tone: Record<ApprovalStatus, BadgeTone> = {
    Approved: "green",
    "Approved with exception": "blue",
    "Awaiting review": "amber",
    Conditional: "amber",
    Blocked: "red",
  };

  return <Badge tone={tone[status]}>{status}</Badge>;
}

export function AssessmentBadge({ status }: { status: AssessmentStatus }) {
  const tone: Record<AssessmentStatus, BadgeTone> = {
    Current: "green",
    "In progress": "blue",
    "Retest required": "amber",
    "Evidence missing": "red",
    "Not started": "slate",
  };

  return <Badge tone={tone[status]}>{status}</Badge>;
}

export function FindingStatusBadge({ status }: { status: FindingStatus }) {
  const tone: Record<FindingStatus, BadgeTone> = {
    New: "red",
    Triage: "amber",
    Assigned: "blue",
    Remediation: "violet",
    "Risk acceptance": "amber",
    "Retest required": "amber",
    Closed: "green",
  };

  return <Badge tone={tone[status]}>{status}</Badge>;
}

export function ReviewStatusBadge({ status }: { status: ReviewStatus }) {
  const tone: Record<ReviewStatus, BadgeTone> = {
    "Ready for review": "blue",
    "Security review required": "amber",
    "Bias review required": "amber",
    "Privacy review required": "amber",
    Approved: "green",
    "Approved with exception": "blue",
    Blocked: "red",
  };

  return <Badge tone={tone[status]}>{status}</Badge>;
}

export function EvidenceBadge({ record }: { record: EvidenceRecord }) {
  return (
    <Badge tone={record.auditPacket ? "green" : "slate"}>
      {record.auditPacket ? "Audit packet" : "Held separately"}
    </Badge>
  );
}
