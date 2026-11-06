"""AI Chatbot API endpoints."""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.chat import ChatMessage, ChatSession
from app.schemas.chat import (
    ChatMessageOut,
    ChatRequest,
    ChatResponseData,
    ChatSessionOut,
)
from app.schemas.common import APIResponse, MetaInfo
from app.services.chatbot_service import ChatbotService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI Chatbot"])
chatbot_service = ChatbotService()


@router.post("/chat", response_model=APIResponse[ChatResponseData])
async def handle_chat_message(
    payload: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    """Send a message to WeatherNext AI chatbot and receive intelligent weather insights."""
    try:
        reply_data = await chatbot_service.handle_message(
            session=session,
            session_id=payload.session_id,
            message=payload.message,
            location_hint=payload.location,
        )
        return APIResponse(
            data=ChatResponseData(**reply_data),
            meta=MetaInfo(
                source="WeatherNext AI Assistant",
                disclaimer="Jawaban asisten berdasarkan data prakiraan cuaca resmi BMKG & WeatherNext AI.",
            ),
        )
    except Exception as exc:
        logger.exception("Error handling chat message: %s", exc)
        raise HTTPException(status_code=500, detail=f"Gagal memproses pesan: {str(exc)}")


@router.get("/chat/{session_id}/history", response_model=APIResponse[list[ChatMessageOut]])
async def get_chat_history(
    session_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Retrieve message history for a chat session."""
    stmt = select(ChatSession).where(ChatSession.session_id == session_id)
    res = await session.execute(stmt)
    chat_session = res.scalar_one_or_none()
    if not chat_session:
        return APIResponse(data=[])

    msg_stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == chat_session.id)
        .order_by(ChatMessage.created_at)
        .limit(50)
    )
    msg_res = await session.execute(msg_stmt)
    messages = list(msg_res.scalars().all())

    return APIResponse(data=[ChatMessageOut.model_validate(m) for m in messages])
