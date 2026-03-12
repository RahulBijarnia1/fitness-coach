from datetime import date, timezone, datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.progress import ProgressLog
from app.schemas.progress_schema import ProgressLogCreate, ProgressLogOut, ProgressHistoryResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.post("/log", response_model=ProgressLogOut, status_code=status.HTTP_201_CREATED)
def create_progress_log(
    payload: ProgressLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    log = ProgressLog(
        user_id=current_user.id,
        weight=payload.weight,
        body_fat=payload.body_fat,
        date=payload.date or datetime.now(timezone.utc).date(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return ProgressLogOut.model_validate(log)


@router.get("/history", response_model=ProgressHistoryResponse)
def get_progress_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(ProgressLog)
        .filter(ProgressLog.user_id == current_user.id)
        .order_by(ProgressLog.date.desc())
    )
    total = query.count()
    logs = query.offset((page - 1) * page_size).limit(page_size).all()

    return ProgressHistoryResponse(
        logs=[ProgressLogOut.model_validate(log) for log in logs],
        total=total,
        page=page,
        page_size=page_size,
    )
