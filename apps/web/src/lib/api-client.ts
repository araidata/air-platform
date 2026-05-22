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

export const apiClient = {
  systems: () => request<ApiSystem[]>("/systems"),
  system: (id: string) => request<ApiSystem>(`/systems/${id}`),
  findings: () => request<ApiFinding[]>("/findings"),
  finding: (id: string) => request<ApiFinding>(`/findings/${id}`),
  evidence: () => request<ApiEvidence[]>("/evidence"),
  evidenceRecord: (id: string) => request<ApiEvidence>(`/evidence/${id}`),
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
};
