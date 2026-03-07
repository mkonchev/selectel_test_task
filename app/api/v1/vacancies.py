from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import vacancy as VacansyService
from app.db.session import get_session
from app.schemas.vacancy import VacancyCreate, VacancyRead, VacancyUpdate

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/", response_model=list[VacancyRead])
async def list_vacancies_endpoint(
    timetable_mode_name: str | None = None,
    city: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[VacancyRead]:
    try:
        return await VacansyService.get_list_vacancy(
            session,
            timetable_mode_name,
            city
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    try:
        vacancy = await (
            VacansyService.get_vacancy(session, vacancy_id)
        )
        return vacancy
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found vacansion with this id: {e}"
        )


@router.post(
    "/",
    response_model=VacancyRead,
    status_code=status.HTTP_201_CREATED
)
async def create_vacancy_endpoint(
    payload: VacancyCreate, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    try:
        vacancy = await (
            VacansyService.create_vacancy(session, payload)
        )
        return vacancy
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # изначально статус был 200_OK # noqa
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: int,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    try:
        vacancy = await (
            VacansyService.update_vacancy(session, vacancy_id, payload)
        )
        return vacancy
    except ValueError as e:  # Опять же можно было содздать кастомное исключение exceptions.VacancyNotFoundError # noqa
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    try:
        await VacansyService.delete_vacancy(session, vacancy_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
