import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession
from app.models.audit import PredictionLog
from app.schemas.predict import PredictRequest, PredictResponse, PredictionRecord
from app.services.predictor import IntentPredictor, get_predictor, hash_message

logger = logging.getLogger(__name__)
router = APIRouter(tags=["predict"])


@router.post(
    "/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_200_OK,
    summary="Classificar mensagem",
    responses={401: {"description": "Token ausente, inválido ou expirado."}},
)
async def predict(
    payload: PredictRequest,
    current_user: CurrentUser,
    db: DbSession,
    predictor: Annotated[IntentPredictor, Depends(get_predictor)],
) -> PredictResponse:
    result = predictor.predict(payload.message, payload.channel)

    # a mensagem em si não é gravada nem logada, só o hash
    record = PredictionLog(
            username=current_user.username,
            message_hash=hash_message(payload.message),
            message_length=len(payload.message),
            predicted_intent=result.intent,
            confidence=result.confidence,
            risk_level=result.risk_level.value,
        )
    db.add(record)
    db.commit()
    db.refresh(record)
    result.prediction_id = record.id

    logger.info(
        "Predição registrada: usuario=%s intent=%s risco=%s",
        current_user.username,
        result.intent,
        result.risk_level.value,
    )
    return result


@router.get("/predictions/{prediction_id}", response_model=PredictionRecord)
async def read_prediction(prediction_id: int, current_user: CurrentUser, db: DbSession):
    # Restrição de ownership faz parte da query parametrizada; não expõe existência.
    record = db.exec(select(PredictionLog).where(
        PredictionLog.id == prediction_id,
        PredictionLog.username == current_user.username,
    )).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Predição não encontrada.")
    return record
