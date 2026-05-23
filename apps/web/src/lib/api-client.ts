const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "/api/backend";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export type ApiSystem = {
  id: string;
  system_name: string;
  department_owner: string;
  business_purpose: string;
  public_facing: boolean;
  rights_impacting: boolean;
  safety_impacting: boolean;
  uses_pii: boolean;
  uses_phi: boolean;
  uses_cjis: boolean;
  model_provider: string | null;
  model_version: string | null;
  deployment_environment: string;
  risk_tier: string;
  approval_status: string;
  target_type: string;
  target_location: string;
  authentication_type: string;
  authentication_reference: string | null;
  assessment_method: string;
  scanner_compatible: string[];
  manual_review_only: boolean;
  uploaded_artifact_supported: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiFinding = {
  id: string;
  system_id: string;
  assessment_id: string;
  scanner_name: string;
  scanner_version: string;
  domain: string;
  severity: string;
  confidence: string;
  title: string;
  description: string;
  evidence_summary: string;
  remediation: string;
  owner_id: string | null;
  status: string;
  due_date: string | null;
  retest_status: string;
  score_impact: Record<string, unknown>;
  risk_accepted: boolean;
  approval_blocking: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiEvidence = {
  id: string;
  finding_id: string | null;
  assessment_id: string | null;
  system_id: string | null;
  evidence_type: string;
  title: string;
  description: string | null;
  file_path: string | null;
  raw_text: string | null;
  content_type: string | null;
  created_by: string;
  created_at: string;
  hash: string | null;
  metadata_json: Record<string, unknown>;
};

export type ApiScoreExplanation = {
  id: string;
  score_id: string;
  explanation_type: string;
  title: string;
  description: string;
  weight: number;
  impact_value: number;
  related_finding_id: string | null;
  created_at: string;
};

export type ApiScore = {
  id: string;
  system_id: string;
  assessment_id: string | null;
  score_domain: string;
  score_value: number;
  weighted_score: number;
  calculated_at: string;
  calculation_version: string;
  created_at: string;
  updated_at: string;
  explanations?: ApiScoreExplanation[];
};

export type ApiScoreHistory = {
  id: string;
  system_id: string;
  assessment_id: string | null;
  score_domain: string;
  previous_score: number | null;
  new_score: number;
  change_reason: string;
  triggered_by: string;
  created_at: string;
};

export type ApiAssessment = {
  id: string;
  system_id: string;
  assessment_type: string;
  initiated_by: string;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  summary: string | null;
  overall_score: number | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type ApiOwner = {
  id: string;
  display_name: string;
  email: string;
  department: string;
  role: string;
  created_at: string;
  updated_at: string;
};

export type ApiAirbReview = {
  id: string;
  system_id: string;
  assessment_id: string | null;
  review_status: string;
  decision_notes: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  exception_granted: boolean;
  expiration_date: string | null;
  civil_rights_review_status: string;
  accessibility_review_status: string;
  language_access_review_status: string;
  fairness_review_status: string;
  human_review_validated: boolean;
  appeal_path_validated: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiScannerDefinition = {
  id: string;
  scanner_name: string;
  display_name: string;
  description: string;
  scanner_category: string;
  adapter_name: string;
  scanner_version: string;
  execution_mode: string;
  supported_domains: string[];
  supported_scan_types: string[];
  enabled: boolean;
  mock_supported: boolean;
  requires_credentials: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiScanType = {
  id: string;
  name: string;
  display_name: string;
  description: string;
  domain: string;
  default_severity: string;
  required_for_risk_tiers: string[];
  applicable_system_types: string[];
  evidence_expectations: string[];
  enabled: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiAssessmentProfile = {
  id: string;
  profile_name: string;
  description: string;
  applicable_risk_tiers: string[];
  applicable_system_types: string[];
  required_scan_types: string[];
  optional_scan_types: string[];
  required_evidence_types: string[];
  recommended_scanners: string[];
  governance_expectations: string[];
  score_domains_affected: string[];
  enabled: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiScannerRun = {
  id: string;
  system_id: string;
  assessment_id: string;
  scanner_definition_id: string;
  scan_type_id: string;
  assessment_profile_id: string | null;
  scanner_name: string;
  scanner_version: string;
  adapter_name: string;
  execution_status: string;
  started_at: string | null;
  completed_at: string | null;
  initiated_by: string;
  raw_output_path: string | null;
  log_path: string | null;
  finding_count: number;
  error_message: string | null;
  created_at: string;
  updated_at: string;
};

export type ApiLanguageAccessScenario = {
  id: string;
  system_id: string | null;
  assessment_id: string | null;
  name: string;
  primary_language: string;
  comparison_language: string;
  scenario_type: string;
  prompt_text: string;
  expected_behavior: string;
  evidence_requirements: string[];
  created_at: string;
  updated_at: string;
};

export type ApiHumanAppealPathCheck = {
  id: string;
  system_id: string;
  assessment_id: string | null;
  check_type: string;
  status: string;
  required_control: string;
  validation_notes: string | null;
  evidence_requirements: string[];
  evidence_ids: string[];
  created_at: string;
  updated_at: string;
};

export type ApiCivilRightsSummary = {
  templates: ApiAssessmentProfile[];
  language_access_scenarios: ApiLanguageAccessScenario[];
  appeal_path_checks: ApiHumanAppealPathCheck[];
  fairness_findings: ApiFinding[];
  fairness_evidence: ApiEvidence[];
};

export type ApiRecommendedScan = {
  scan_type: ApiScanType;
  required: boolean;
  reason: string;
  available_scanners: ApiScannerDefinition[];
};

export type ApiScanRecommendations = {
  system_id: string;
  risk_tier: string;
  assessment_profile: ApiAssessmentProfile | null;
  required_scans: ApiRecommendedScan[];
  optional_scans: ApiRecommendedScan[];
};

export const apiClient = {
  systems: () => request<ApiSystem[]>("/systems"),
  system: (id: string) => request<ApiSystem>(`/systems/${id}`),
  createSystem: (payload: {
    system_name: string;
    department_owner: string;
    business_purpose: string;
    public_facing: boolean;
    rights_impacting: boolean;
    safety_impacting: boolean;
    uses_pii: boolean;
    uses_phi: boolean;
    uses_cjis: boolean;
    model_provider?: string | null;
    model_version?: string | null;
    deployment_environment: string;
    risk_tier: string;
    approval_status: string;
    target_type: string;
    target_location: string;
    authentication_type: string;
    authentication_reference?: string | null;
    assessment_method: string;
    scanner_compatible: string[];
    manual_review_only: boolean;
    uploaded_artifact_supported: boolean;
  }) =>
    request<ApiSystem>("/systems", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateSystem: (id: string, payload: Partial<Omit<ApiSystem, "id" | "created_at" | "updated_at">>) =>
    request<ApiSystem>(`/systems/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  findings: () => request<ApiFinding[]>("/findings"),
  finding: (id: string) => request<ApiFinding>(`/findings/${id}`),
  updateFinding: (
    id: string,
    payload: Partial<
      Pick<
        ApiFinding,
        | "owner_id"
        | "due_date"
        | "remediation"
        | "approval_blocking"
        | "severity"
        | "domain"
      >
    > & { actor?: string; notes?: string },
  ) =>
    request<ApiFinding>(`/findings/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  transitionFinding: (
    id: string,
    payload: {
      status: string;
      actor: string;
      notes?: string;
      risk_acceptance_rationale?: string;
    },
  ) =>
    request<ApiFinding>(`/findings/${id}/transition`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  createRetest: (
    findingId: string,
    payload: {
      initiated_by: string;
      status?: string;
      notes?: string;
      result_summary?: string;
    },
  ) =>
    request<{ id: string; finding_id: string; status: string }>(`/findings/${findingId}/retest`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  evidence: () => request<ApiEvidence[]>("/evidence"),
  evidenceRecord: (id: string) => request<ApiEvidence>(`/evidence/${id}`),
  assessments: () => request<ApiAssessment[]>("/assessments"),
  createAssessment: (payload: {
    system_id: string;
    assessment_type: string;
    initiated_by: string;
    status?: string;
    started_at?: string;
    summary?: string;
    notes?: string;
  }) =>
    request<ApiAssessment>("/assessments", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  owners: () => request<ApiOwner[]>("/owners"),
  airbReviews: () => request<ApiAirbReview[]>("/airb-reviews"),
  createAirbReview: (payload: {
    system_id: string;
    assessment_id?: string | null;
    review_status?: string;
    decision_notes?: string;
    reviewed_by?: string;
    exception_granted?: boolean;
    expiration_date?: string | null;
    civil_rights_review_status?: string;
    accessibility_review_status?: string;
    language_access_review_status?: string;
    fairness_review_status?: string;
    human_review_validated?: boolean;
    appeal_path_validated?: boolean;
    actor?: string;
  }) =>
    request<ApiAirbReview>("/airb-reviews", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateAirbReview: (
    id: string,
    payload: Partial<
      Pick<
        ApiAirbReview,
        | "review_status"
        | "decision_notes"
        | "reviewed_by"
        | "reviewed_at"
        | "exception_granted"
        | "expiration_date"
        | "civil_rights_review_status"
        | "accessibility_review_status"
        | "language_access_review_status"
        | "fairness_review_status"
        | "human_review_validated"
        | "appeal_path_validated"
      >
    > & { actor?: string },
  ) =>
    request<ApiAirbReview>(`/airb-reviews/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  scores: () => request<ApiScore[]>("/scores"),
  score: (id: string) => request<ApiScore>(`/scores/${id}`),
  systemScores: (id: string) => request<ApiScore[]>(`/systems/${id}/scores`),
  scoreExplanations: (id: string) =>
    request<ApiScoreExplanation[]>(`/scores/${id}/explanations`),
  systemScoreHistory: (id: string) =>
    request<ApiScoreHistory[]>(`/systems/${id}/score-history`),
  recalculateSystemScores: (id: string, triggeredBy = "operator") =>
    request<{ system_id: string; assessment_id: string | null; scores: ApiScore[] }>(
      `/systems/${id}/recalculate-scores`,
      {
        method: "POST",
        body: JSON.stringify({
          triggered_by: triggeredBy,
          change_reason: "frontend requested score recalculation",
        }),
      },
    ),
  scannerDefinitions: () => request<ApiScannerDefinition[]>("/scanner-definitions"),
  scanTypes: () => request<ApiScanType[]>("/scan-types"),
  assessmentProfiles: () => request<ApiAssessmentProfile[]>("/assessment-profiles"),
  scannerRuns: () => request<ApiScannerRun[]>("/scanner-runs"),
  systemScannerRuns: (id: string) => request<ApiScannerRun[]>(`/systems/${id}/scanner-runs`),
  recommendedScans: (systemId: string, profileId?: string) => {
    const query = profileId ? `?assessment_profile_id=${profileId}` : "";
    return request<ApiScanRecommendations>(`/systems/${systemId}/recommended-scans${query}`);
  },
  createScannerRun: (payload: {
    system_id: string;
    assessment_id?: string;
    scanner_definition_id: string;
    scan_type_id: string;
    assessment_profile_id?: string;
    initiated_by?: string;
  }) =>
    request<ApiScannerRun>("/scanner-runs", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  executeScannerRun: (id: string, initiatedBy = "operator") =>
    request<ApiScannerRun>(`/scanner-runs/${id}/execute`, {
      method: "POST",
      body: JSON.stringify({ initiated_by: initiatedBy }),
    }),
  civilRightsSummary: () => request<ApiCivilRightsSummary>("/civil-rights/summary"),
};
