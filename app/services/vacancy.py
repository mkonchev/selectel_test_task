import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import vacancy as VacancyCRUD
from app.schemas import vacancy as schema_vacancy


async def get_vacancy(session: AsyncSession, vacancy_id: int):
    vacancy_db = await (
        VacancyCRUD.get_vacancy(session, vacancy_id)
    )
    if not vacancy_db:
        raise ValueError(
            "Vacancy with this id doesn't exists"
        )  # тут можно было написать кастомное исключение, но тк нам нужно минимально переделать, а не писать новое, то оставим так # noqa
    return vacancy_db


async def get_list_vacancy(session: AsyncSession, mode_name: str, city: str):
    try:
        return await VacancyCRUD.list_vacancies(session, mode_name, city)
    except Exception as e:
        logging.error(f"Failed to get list[Vacancies]: {e}")
        raise


async def create_vacancy(
    session: AsyncSession,
    payload: schema_vacancy.VacancyCreate
):
    if payload.external_id is not None:
        existing = await (
            VacancyCRUD.get_vacancy_by_external_id(
                session,
                payload.external_id
            )
        )
        if existing:
            raise ValueError(
                "Vacancy with this external_id already exists"
            )
    try:
        vacancy = await VacancyCRUD.create_vacancy(session, payload)
        return vacancy
    except Exception as e:
        logging.error(f"Failed to create vacancy: {e}")


async def update_vacancy(
    session: AsyncSession,
    vacancy_id: int,
    payload: schema_vacancy.VacancyUpdate
):
    existing = await (
        VacancyCRUD.get_vacancy(session, vacancy_id)
    )
    if not existing:
        raise ValueError(
            "No vacancy with this id"
        )
    try:
        vacancy = await VacancyCRUD.update_vacancy(session, existing, payload)
        return vacancy
    except Exception as e:
        logging.error(f"Failed to update vacancy: {e}")
        raise


async def delete_vacancy(
        session: AsyncSession,
        vacancy_id: int
):
    vacancy = await VacancyCRUD.get_vacancy(session, vacancy_id)
    if not vacancy:
        raise ValueError(
            "No vacansy with this id"
        )
    try:
        return await VacancyCRUD.delete_vacancy(session, vacancy)
    except Exception as e:
        logging.error(f"Failed to delete vacancy {vacancy_id}: {e}")
        raise
