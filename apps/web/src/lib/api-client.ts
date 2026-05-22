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
  findings: () => request<ApiFinding[]>("/findings"),
  finding: (id: string) => request<ApiFinding>(`/findings/${id}`),
  evidence: () => request<ApiEvidence[]>("/evidence"),
  evidenceRecord: (id: string) => request<ApiEvidence>(`/evidence/${id}`),
  assessments: () => request<ApiAssessment[]>("/assessments"),
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
};
