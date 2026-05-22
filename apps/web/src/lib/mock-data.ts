export type RiskTier = "Critical" | "High" | "Medium" | "Low";
export type ApprovalStatus =
  | "Approved"
  | "Approved with exception"
  | "Awaiting review"
  | "Conditional"
  | "Blocked";
export type AssessmentStatus =
  | "Current"
  | "In progress"
  | "Retest required"
  | "Evidence missing"
  | "Not started";
export type FindingSeverity = "Critical" | "High" | "Medium" | "Low";
export type FindingStatus =
  | "New"
  | "Triage"
  | "Assigned"
  | "Remediation"
  | "Risk acceptance"
  | "Retest required"
  | "Closed";
export type FindingDomain =
  | "Security"
  | "Bias and Civil Rights"
  | "Privacy"
  | "Governance"
  | "Audit";
export type ScoreDomain =
  | "Security"
  | "Privacy"
  | "Bias and Civil Rights"
  | "Explainability"
  | "Governance Evidence"
  | "Overall Governance";
export type EvidenceType =
  | "Assessment"
  | "Scanner output"
  | "Policy"
  | "Decision"
  | "Retest"
  | "Data sample";
export type ReviewStatus =
  | "Ready for review"
  | "Security review required"
  | "Bias review required"
  | "Privacy review required"
  | "Approved"
  | "Approved with exception"
  | "Blocked";

export type AiSystem = {
  id: string;
  name: string;
  department: string;
  owner: string;
  purpose: string;
  riskTier: RiskTier;
  approvalStatus: ApprovalStatus;
  assessmentStatus: AssessmentStatus;
  reviewStatus: ReviewStatus;
  publicFacing: boolean;
  rightsImpacting: boolean;
  safetyImpacting: boolean;
  dataTypes: string[];
  riskScore: number;
  evidenceCompleteness: number;
  lastAssessed: string;
  nextReview: string;
  deploymentStatus: string;
  domains: {
    security: number;
    biasCivilRights: number;
    privacy: number;
    explainability: number;
    governanceEvidence: number;
  };
};

export type Finding = {
  id: string;
  systemId: string;
  title: string;
  severity: FindingSeverity;
  status: FindingStatus;
  domain: FindingDomain;
  owner: string;
  dueDate: string;
  confidence: "High" | "Medium" | "Low";
  scoreImpact: number;
  summary: string;
  evidenceIds: string[];
  frameworkMappings: string[];
};

export type EvidenceRecord = {
  id: string;
  systemId: string;
  title: string;
  type: EvidenceType;
  collectedAt: string;
  source: string;
  hash: string;
  sensitivity: "Public" | "Internal" | "Confidential" | "Restricted";
  auditPacket: boolean;
  linkedFindingIds: string[];
  summary: string;
};

export type Assessment = {
  id: string;
  systemId: string;
  name: string;
  status: AssessmentStatus;
  assessor: string;
  completedAt: string;
  evidenceComplete: boolean;
};

export type Review = {
  id: string;
  systemId: string;
  status: ReviewStatus;
  requestedBy: string;
  meetingDate: string;
  decision: string;
  blockers: string[];
  evidenceIds: string[];
};

export type ScoreExplanation = {
  id: string;
  systemId: string;
  domain: ScoreDomain;
  title: string;
  description: string;
  impact: number;
  relatedFindingId?: string;
};

export type ScoreHistoryPoint = {
  systemId: string;
  label: string;
  overall: number;
  security: number;
  privacy: number;
  biasCivilRights: number;
  explainability: number;
  governanceEvidence: number;
};

export const systems: AiSystem[] = [
  {
    id: "public-benefits-chatbot",
    name: "Public Benefits Chatbot",
    department: "Health and Human Services",
    owner: "Maria Chen",
    purpose:
      "Answers benefits eligibility questions and routes residents to county assistance programs.",
    riskTier: "High",
    approvalStatus: "Conditional",
    assessmentStatus: "Retest required",
    reviewStatus: "Security review required",
    publicFacing: true,
    rightsImpacting: true,
    safetyImpacting: false,
    dataTypes: ["PII", "Benefits eligibility", "Language access"],
    riskScore: 61,
    evidenceCompleteness: 72,
    lastAssessed: "2026-05-10",
    nextReview: "2026-06-04",
    deploymentStatus: "Limited pilot",
    domains: {
      security: 58,
      biasCivilRights: 54,
      privacy: 71,
      explainability: 62,
      governanceEvidence: 57,
    },
  },
  {
    id: "sheriff-incident-summary",
    name: "Sheriff Incident Summary Assistant",
    department: "Sheriff's Office",
    owner: "Derek Lawson",
    purpose:
      "Drafts incident report summaries from officer notes for supervisor review.",
    riskTier: "Critical",
    approvalStatus: "Blocked",
    assessmentStatus: "Evidence missing",
    reviewStatus: "Blocked",
    publicFacing: false,
    rightsImpacting: true,
    safetyImpacting: true,
    dataTypes: ["CJIS", "PII", "Law enforcement records"],
    riskScore: 43,
    evidenceCompleteness: 38,
    lastAssessed: "2026-05-08",
    nextReview: "2026-05-28",
    deploymentStatus: "Deployment blocked",
    domains: {
      security: 39,
      biasCivilRights: 46,
      privacy: 42,
      explainability: 48,
      governanceEvidence: 41,
    },
  },
  {
    id: "permit-review-assistant",
    name: "Permit Review Assistant",
    department: "Planning and Development",
    owner: "Nisha Patel",
    purpose:
      "Summarizes permit applications, flags missing documents, and prepares review notes.",
    riskTier: "Medium",
    approvalStatus: "Approved",
    assessmentStatus: "Current",
    reviewStatus: "Approved",
    publicFacing: false,
    rightsImpacting: false,
    safetyImpacting: false,
    dataTypes: ["Permit records", "Property records"],
    riskScore: 82,
    evidenceCompleteness: 91,
    lastAssessed: "2026-05-14",
    nextReview: "2026-08-12",
    deploymentStatus: "Production",
    domains: {
      security: 84,
      biasCivilRights: 87,
      privacy: 79,
      explainability: 86,
      governanceEvidence: 91,
    },
  },
  {
    id: "hr-resume-screening",
    name: "HR Resume Screening AI",
    department: "Human Resources",
    owner: "Elena Brooks",
    purpose:
      "Ranks application materials for minimum qualifications before human hiring review.",
    riskTier: "High",
    approvalStatus: "Awaiting review",
    assessmentStatus: "In progress",
    reviewStatus: "Bias review required",
    publicFacing: false,
    rightsImpacting: true,
    safetyImpacting: false,
    dataTypes: ["Employment records", "Applicant PII"],
    riskScore: 55,
    evidenceCompleteness: 64,
    lastAssessed: "2026-05-12",
    nextReview: "2026-05-30",
    deploymentStatus: "Pre-deployment review",
    domains: {
      security: 69,
      biasCivilRights: 41,
      privacy: 62,
      explainability: 52,
      governanceEvidence: 49,
    },
  },
  {
    id: "citizen-services-rag",
    name: "Citizen Services RAG Chatbot",
    department: "County IT",
    owner: "Owen Ramirez",
    purpose:
      "Uses approved county knowledge base content to answer 311 service questions.",
    riskTier: "Medium",
    approvalStatus: "Approved with exception",
    assessmentStatus: "Retest required",
    reviewStatus: "Approved with exception",
    publicFacing: true,
    rightsImpacting: false,
    safetyImpacting: false,
    dataTypes: ["Service requests", "Knowledge base"],
    riskScore: 74,
    evidenceCompleteness: 83,
    lastAssessed: "2026-05-16",
    nextReview: "2026-07-15",
    deploymentStatus: "Production with exception",
    domains: {
      security: 68,
      biasCivilRights: 80,
      privacy: 76,
      explainability: 74,
      governanceEvidence: 72,
    },
  },
];

export const findings: Finding[] = [
  {
    id: "FND-001",
    systemId: "public-benefits-chatbot",
    title: "Prompt injection vulnerability",
    severity: "Critical",
    status: "Retest required",
    domain: "Security",
    owner: "Avery Stone",
    dueDate: "2026-05-29",
    confidence: "High",
    scoreImpact: -18,
    summary:
      "Adversarial instructions caused the assistant to ignore benefit-program guardrails in two mock scenarios.",
    evidenceIds: ["EVD-001", "EVD-002"],
    frameworkMappings: ["NIST AI RMF: Map", "OWASP LLM: LLM01"],
  },
  {
    id: "FND-002",
    systemId: "public-benefits-chatbot",
    title: "Spanish-language explanation disparity",
    severity: "High",
    status: "Assigned",
    domain: "Bias and Civil Rights",
    owner: "Jules Rivera",
    dueDate: "2026-06-03",
    confidence: "Medium",
    scoreImpact: -14,
    summary:
      "Spanish responses omitted appeal-path language present in English eligibility explanations.",
    evidenceIds: ["EVD-003"],
    frameworkMappings: ["Title VI", "NIST AI RMF: Measure"],
  },
  {
    id: "FND-003",
    systemId: "hr-resume-screening",
    title: "Missing human appeal path",
    severity: "High",
    status: "Triage",
    domain: "Governance",
    owner: "Morgan Lee",
    dueDate: "2026-05-31",
    confidence: "High",
    scoreImpact: -16,
    summary:
      "Applicant workflow lacks documented notice and appeal language for AI-assisted ranking decisions.",
    evidenceIds: ["EVD-004"],
    frameworkMappings: ["EEOC AI Guidance", "NIST AI RMF: Govern"],
  },
  {
    id: "FND-004",
    systemId: "citizen-services-rag",
    title: "Excessive MCP/tool permissions",
    severity: "High",
    status: "Remediation",
    domain: "Security",
    owner: "Riley Hart",
    dueDate: "2026-05-27",
    confidence: "High",
    scoreImpact: -12,
    summary:
      "The assistant test profile exposed write-capable tool permissions not required for public service lookups.",
    evidenceIds: ["EVD-005"],
    frameworkMappings: ["OWASP LLM: LLM06", "County AI Standard: Tooling"],
  },
  {
    id: "FND-005",
    systemId: "sheriff-incident-summary",
    title: "Incomplete audit logging",
    severity: "High",
    status: "Assigned",
    domain: "Audit",
    owner: "Avery Stone",
    dueDate: "2026-05-26",
    confidence: "High",
    scoreImpact: -15,
    summary:
      "Draft generation events do not retain prompt, source note references, reviewer, and approval timestamps together.",
    evidenceIds: ["EVD-006"],
    frameworkMappings: ["CJIS Policy", "NIST AI RMF: Govern"],
  },
  {
    id: "FND-006",
    systemId: "sheriff-incident-summary",
    title: "Possible sensitive data leakage",
    severity: "Critical",
    status: "New",
    domain: "Privacy",
    owner: "Priya Nair",
    dueDate: "2026-05-24",
    confidence: "Medium",
    scoreImpact: -20,
    summary:
      "Mock prompt replay produced a summary containing restricted personal details not needed for the intended report excerpt.",
    evidenceIds: ["EVD-007"],
    frameworkMappings: ["CJIS Policy", "NIST Privacy Framework"],
  },
  {
    id: "FND-007",
    systemId: "hr-resume-screening",
    title: "Weak governance evidence",
    severity: "Medium",
    status: "Risk acceptance",
    domain: "Governance",
    owner: "Morgan Lee",
    dueDate: "2026-06-07",
    confidence: "Medium",
    scoreImpact: -8,
    summary:
      "Business owner attestation exists, but selection-criteria review and model-change signoff are incomplete.",
    evidenceIds: ["EVD-008"],
    frameworkMappings: ["NIST AI RMF: Govern"],
  },
  {
    id: "FND-008",
    systemId: "citizen-services-rag",
    title: "Missing risk acceptance",
    severity: "Medium",
    status: "Triage",
    domain: "Governance",
    owner: "Riley Hart",
    dueDate: "2026-06-02",
    confidence: "High",
    scoreImpact: -7,
    summary:
      "Approved exception for stale knowledge-base answers does not yet have owner, expiration, and compensating control evidence.",
    evidenceIds: ["EVD-009"],
    frameworkMappings: ["County AI Standard: Exceptions"],
  },
  {
    id: "FND-009",
    systemId: "permit-review-assistant",
    title: "Missing retest documentation",
    severity: "Low",
    status: "Closed",
    domain: "Audit",
    owner: "Sam Taylor",
    dueDate: "2026-05-22",
    confidence: "High",
    scoreImpact: -3,
    summary:
      "Closure was approved after retest notes were attached to the assessment packet.",
    evidenceIds: ["EVD-010"],
    frameworkMappings: ["NIST AI RMF: Manage"],
  },
];

export const evidenceRecords: EvidenceRecord[] = [
  {
    id: "EVD-001",
    systemId: "public-benefits-chatbot",
    title: "Prompt injection red-team transcript",
    type: "Scanner output",
    collectedAt: "2026-05-10",
    source: "Mock prompt injection assessment",
    hash: "sha256:9c1a4f2b",
    sensitivity: "Internal",
    auditPacket: true,
    linkedFindingIds: ["FND-001"],
    summary: "Raw transcript for two bypass attempts and model responses.",
  },
  {
    id: "EVD-002",
    systemId: "public-benefits-chatbot",
    title: "Retest script and expected guardrail behavior",
    type: "Retest",
    collectedAt: "2026-05-18",
    source: "Assurance operator",
    hash: "sha256:45e90b91",
    sensitivity: "Internal",
    auditPacket: true,
    linkedFindingIds: ["FND-001"],
    summary: "Retest scenarios awaiting owner confirmation.",
  },
  {
    id: "EVD-003",
    systemId: "public-benefits-chatbot",
    title: "Language access response comparison",
    type: "Assessment",
    collectedAt: "2026-05-11",
    source: "Civil rights review checklist",
    hash: "sha256:0de34a6c",
    sensitivity: "Internal",
    auditPacket: true,
    linkedFindingIds: ["FND-002"],
    summary: "English and Spanish explanation samples with reviewer notes.",
  },
  {
    id: "EVD-004",
    systemId: "hr-resume-screening",
    title: "Applicant notice workflow capture",
    type: "Policy",
    collectedAt: "2026-05-12",
    source: "HR process review",
    hash: "sha256:7a76e1bd",
    sensitivity: "Confidential",
    auditPacket: true,
    linkedFindingIds: ["FND-003"],
    summary: "Current applicant communications and missing AI appeal language.",
  },
  {
    id: "EVD-005",
    systemId: "citizen-services-rag",
    title: "Tool permission export",
    type: "Assessment",
    collectedAt: "2026-05-16",
    source: "Mock configuration review",
    hash: "sha256:531afdd0",
    sensitivity: "Internal",
    auditPacket: true,
    linkedFindingIds: ["FND-004"],
    summary: "Tool list showing unused write permissions in the public profile.",
  },
  {
    id: "EVD-006",
    systemId: "sheriff-incident-summary",
    title: "Audit log sample",
    type: "Data sample",
    collectedAt: "2026-05-08",
    source: "Sheriff's Office pilot environment",
    hash: "sha256:1120ac74",
    sensitivity: "Restricted",
    auditPacket: true,
    linkedFindingIds: ["FND-005"],
    summary: "Sample event export with missing reviewer and source references.",
  },
  {
    id: "EVD-007",
    systemId: "sheriff-incident-summary",
    title: "Restricted detail replay output",
    type: "Scanner output",
    collectedAt: "2026-05-08",
    source: "Mock privacy probe",
    hash: "sha256:bb65ca91",
    sensitivity: "Restricted",
    auditPacket: false,
    linkedFindingIds: ["FND-006"],
    summary: "Raw output retained as restricted evidence outside board packet.",
  },
  {
    id: "EVD-008",
    systemId: "hr-resume-screening",
    title: "Selection criteria attestation",
    type: "Decision",
    collectedAt: "2026-05-13",
    source: "HR owner attestation",
    hash: "sha256:407be020",
    sensitivity: "Confidential",
    auditPacket: true,
    linkedFindingIds: ["FND-007"],
    summary: "Business-owner attestation with missing model-change signoff.",
  },
  {
    id: "EVD-009",
    systemId: "citizen-services-rag",
    title: "Knowledge-base exception memo",
    type: "Decision",
    collectedAt: "2026-05-15",
    source: "AI Review Board notes",
    hash: "sha256:db5e1091",
    sensitivity: "Internal",
    auditPacket: false,
    linkedFindingIds: ["FND-008"],
    summary: "Draft exception memo pending owner and expiration date.",
  },
  {
    id: "EVD-010",
    systemId: "permit-review-assistant",
    title: "Retest closure note",
    type: "Retest",
    collectedAt: "2026-05-14",
    source: "Planning assessment",
    hash: "sha256:61cd0fee",
    sensitivity: "Internal",
    auditPacket: true,
    linkedFindingIds: ["FND-009"],
    summary: "Retest note confirming audit packet update before closure.",
  },
];

export const assessments: Assessment[] = [
  {
    id: "ASM-001",
    systemId: "public-benefits-chatbot",
    name: "Public-facing assistant security and language access review",
    status: "Retest required",
    assessor: "Avery Stone",
    completedAt: "2026-05-10",
    evidenceComplete: false,
  },
  {
    id: "ASM-002",
    systemId: "sheriff-incident-summary",
    name: "CJIS, privacy, and safety-impact review",
    status: "Evidence missing",
    assessor: "Priya Nair",
    completedAt: "2026-05-08",
    evidenceComplete: false,
  },
  {
    id: "ASM-003",
    systemId: "permit-review-assistant",
    name: "Operational governance review",
    status: "Current",
    assessor: "Sam Taylor",
    completedAt: "2026-05-14",
    evidenceComplete: true,
  },
  {
    id: "ASM-004",
    systemId: "hr-resume-screening",
    name: "Employment decision civil-rights review",
    status: "In progress",
    assessor: "Jules Rivera",
    completedAt: "2026-05-12",
    evidenceComplete: false,
  },
  {
    id: "ASM-005",
    systemId: "citizen-services-rag",
    name: "RAG public service security review",
    status: "Retest required",
    assessor: "Riley Hart",
    completedAt: "2026-05-16",
    evidenceComplete: true,
  },
];

export const reviews: Review[] = [
  {
    id: "AIRB-001",
    systemId: "public-benefits-chatbot",
    status: "Security review required",
    requestedBy: "Maria Chen",
    meetingDate: "2026-06-04",
    decision: "Conditional pilot remains open pending retest evidence.",
    blockers: ["Prompt injection retest", "Spanish appeal language update"],
    evidenceIds: ["EVD-001", "EVD-002", "EVD-003"],
  },
  {
    id: "AIRB-002",
    systemId: "sheriff-incident-summary",
    status: "Blocked",
    requestedBy: "Derek Lawson",
    meetingDate: "2026-05-28",
    decision: "Deployment blocked until audit logging and privacy evidence are complete.",
    blockers: ["Restricted data leakage", "Incomplete audit logging"],
    evidenceIds: ["EVD-006", "EVD-007"],
  },
  {
    id: "AIRB-003",
    systemId: "permit-review-assistant",
    status: "Approved",
    requestedBy: "Nisha Patel",
    meetingDate: "2026-05-20",
    decision: "Approved for production with quarterly review.",
    blockers: [],
    evidenceIds: ["EVD-010"],
  },
  {
    id: "AIRB-004",
    systemId: "hr-resume-screening",
    status: "Bias review required",
    requestedBy: "Elena Brooks",
    meetingDate: "2026-05-30",
    decision: "Board packet incomplete pending appeal-path evidence.",
    blockers: ["Human appeal path", "Selection criteria signoff"],
    evidenceIds: ["EVD-004", "EVD-008"],
  },
  {
    id: "AIRB-005",
    systemId: "citizen-services-rag",
    status: "Approved with exception",
    requestedBy: "Owen Ramirez",
    meetingDate: "2026-05-22",
    decision: "Approved with exception for knowledge-base freshness controls.",
    blockers: ["Risk acceptance expiration date"],
    evidenceIds: ["EVD-005", "EVD-009"],
  },
];

export const scoreExplanations: ScoreExplanation[] = [
  {
    id: "SCX-001",
    systemId: "public-benefits-chatbot",
    domain: "Security",
    title: "Critical prompt injection exposure",
    description:
      "Prompt injection retest remains open and deployment approval is blocked until guardrail evidence is attached.",
    impact: -18,
    relatedFindingId: "FND-001",
  },
  {
    id: "SCX-002",
    systemId: "public-benefits-chatbot",
    domain: "Bias and Civil Rights",
    title: "Language access disparity",
    description:
      "Spanish-language benefit explanations omitted appeal-path details that are present in English responses.",
    impact: -14,
    relatedFindingId: "FND-002",
  },
  {
    id: "SCX-003",
    systemId: "sheriff-incident-summary",
    domain: "Governance Evidence",
    title: "Audit trail incomplete",
    description:
      "Reviewer, source note, and approval timestamp evidence are not preserved together for incident summaries.",
    impact: -15,
    relatedFindingId: "FND-005",
  },
  {
    id: "SCX-004",
    systemId: "sheriff-incident-summary",
    domain: "Privacy",
    title: "Restricted data leakage",
    description:
      "Mock replay output included personal details beyond the intended report excerpt.",
    impact: -20,
    relatedFindingId: "FND-006",
  },
  {
    id: "SCX-005",
    systemId: "permit-review-assistant",
    domain: "Governance Evidence",
    title: "Evidence packet complete",
    description:
      "Retest closure and board approval notes are linked to the current assessment packet.",
    impact: 6,
    relatedFindingId: "FND-009",
  },
  {
    id: "SCX-006",
    systemId: "hr-resume-screening",
    domain: "Bias and Civil Rights",
    title: "Human appeal path missing",
    description:
      "Applicant notice and appeal language are not yet documented for the AI-assisted ranking workflow.",
    impact: -16,
    relatedFindingId: "FND-003",
  },
  {
    id: "SCX-007",
    systemId: "hr-resume-screening",
    domain: "Governance Evidence",
    title: "Model-change signoff incomplete",
    description:
      "Selection-criteria review exists, but model-change signoff is not complete enough for board approval.",
    impact: -8,
    relatedFindingId: "FND-007",
  },
  {
    id: "SCX-008",
    systemId: "citizen-services-rag",
    domain: "Security",
    title: "Excessive tool permissions",
    description:
      "Write-capable tool permissions remain enabled in a public-service lookup profile.",
    impact: -12,
    relatedFindingId: "FND-004",
  },
  {
    id: "SCX-009",
    systemId: "citizen-services-rag",
    domain: "Governance Evidence",
    title: "Risk acceptance metadata missing",
    description:
      "The knowledge-base freshness exception needs an owner, expiration date, and compensating control evidence.",
    impact: -7,
    relatedFindingId: "FND-008",
  },
];

export const scoreHistory: ScoreHistoryPoint[] = systems.flatMap((system) => {
  const baselines = [
    Math.max(0, system.riskScore + 7),
    Math.max(0, system.riskScore + 4),
    Math.max(0, system.riskScore + 2),
    system.riskScore,
  ];
  const labels = ["Feb", "Mar", "Apr", "May"];

  return labels.map((label, index) => ({
    systemId: system.id,
    label,
    overall: baselines[index],
    security: Math.max(0, Math.min(100, system.domains.security + (3 - index) * 2)),
    privacy: Math.max(0, Math.min(100, system.domains.privacy + (3 - index))),
    biasCivilRights: Math.max(
      0,
      Math.min(100, system.domains.biasCivilRights + (3 - index) * 2),
    ),
    explainability: Math.max(
      0,
      Math.min(100, system.domains.explainability + (3 - index) * 2),
    ),
    governanceEvidence: Math.max(
      0,
      Math.min(100, system.domains.governanceEvidence + (3 - index) * 2),
    ),
  }));
});

export const formatDate = (value: string) =>
  new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));

export function getSystemById(id: string) {
  return systems.find((system) => system.id === id);
}

export function getFindingsForSystem(systemId: string) {
  return findings.filter((finding) => finding.systemId === systemId);
}

export function getEvidenceForSystem(systemId: string) {
  return evidenceRecords.filter((evidence) => evidence.systemId === systemId);
}

export function getAssessmentsForSystem(systemId: string) {
  return assessments.filter((assessment) => assessment.systemId === systemId);
}

export function getReviewForSystem(systemId: string) {
  return reviews.find((review) => review.systemId === systemId);
}

export function getScoreExplanationsForSystem(systemId: string) {
  return scoreExplanations.filter((explanation) => explanation.systemId === systemId);
}

export function getScoreHistoryForSystem(systemId: string) {
  return scoreHistory.filter((point) => point.systemId === systemId);
}

export function getSystemName(systemId: string) {
  return getSystemById(systemId)?.name ?? "Unknown system";
}

export const openFindings = findings.filter(
  (finding) => finding.status !== "Closed",
);

export const dashboardMetrics = {
  averageRiskScore: Math.round(
    systems.reduce((sum, system) => sum + system.riskScore, 0) / systems.length,
  ),
  openFindings: openFindings.length,
  blockedSystems: systems.filter((system) => system.approvalStatus === "Blocked")
    .length,
  evidenceCompleteness: Math.round(
    systems.reduce((sum, system) => sum + system.evidenceCompleteness, 0) /
      systems.length,
  ),
  awaitingReview: reviews.filter((review) =>
    [
      "Ready for review",
      "Security review required",
      "Bias review required",
      "Privacy review required",
      "Blocked",
    ].includes(review.status),
  ).length,
};

export const riskHeatmap = [
  {
    department: "Health and Human Services",
    security: 58,
    biasCivilRights: 54,
    privacy: 71,
    explainability: 62,
    governanceEvidence: 57,
  },
  {
    department: "Sheriff's Office",
    security: 39,
    biasCivilRights: 46,
    privacy: 42,
    explainability: 48,
    governanceEvidence: 41,
  },
  {
    department: "Planning and Development",
    security: 84,
    biasCivilRights: 87,
    privacy: 79,
    explainability: 86,
    governanceEvidence: 91,
  },
  {
    department: "Human Resources",
    security: 69,
    biasCivilRights: 41,
    privacy: 62,
    explainability: 52,
    governanceEvidence: 49,
  },
  {
    department: "County IT",
    security: 68,
    biasCivilRights: 80,
    privacy: 76,
    explainability: 74,
    governanceEvidence: 72,
  },
];

export const scoreTrend = [
  { label: "Feb", score: 68 },
  { label: "Mar", score: 65 },
  { label: "Apr", score: 67 },
  { label: "May", score: dashboardMetrics.averageRiskScore },
];
