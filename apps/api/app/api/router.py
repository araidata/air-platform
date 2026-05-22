from fastapi import APIRouter

from app.api.routes import (
    airb_reviews,
    assessments,
    audit_events,
    evidence,
    findings,
    owners,
    retests,
    scores,
    scanners,
    systems,
)

api_router = APIRouter()
api_router.include_router(systems.router, prefix="/systems", tags=["systems"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(findings.router, prefix="/findings", tags=["findings"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
api_router.include_router(audit_events.router, prefix="/audit-events", tags=["audit"])
api_router.include_router(retests.router, tags=["retests"])
api_router.include_router(airb_reviews.router, prefix="/airb-reviews", tags=["airb"])
api_router.include_router(owners.router, prefix="/owners", tags=["owners"])
api_router.include_router(scores.router, tags=["scores"])
api_router.include_router(scanners.router, tags=["scanners"])
