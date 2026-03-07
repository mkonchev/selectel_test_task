from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.parser import parse_and_store
from app.db.session import get_session
from app.schemas import external as schemas

router = APIRouter(prefix="/parse", tags=["parser"])


@router.post("/")
async def parse_endpoint(
    session: AsyncSession = Depends(get_session)
) -> schemas.ExternalParseResponce:
    created_count = await parse_and_store(session)
    return {"item_count": created_count}
