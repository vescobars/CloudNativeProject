""" Utils for users """
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.exceptions import UniqueConstraintViolatedException, UtilityNotFoundException
from src.models import Utility
from src.schemas import UtilitySchema


class Utilities:

    @staticmethod
    def create_utility(offer_id: str, utility: float, session: Session) -> UtilitySchema:
        """
        Insert a new utility into the Utilities table
        """
        new_utility = None
        with session:
            current_time = datetime.now(timezone.utc)
            try:
                new_utility = Utility(
                    offer_id=offer_id,
                    utility=utility,
                    createdAt=current_time,
                    updateAt=current_time
                )

                session.add(new_utility)
                session.commit()
            except IntegrityError as e:
                raise UniqueConstraintViolatedException(e)
        return new_utility

    @staticmethod
    def update_utility(offer_id: str, utility: float, sess: Session) -> bool:
        try:
            retrieved_utility = sess.execute(
                select(Utility).where(Utility.id == offer_id)
            ).scalar_one()

            updated = False
            if retrieved_utility.utility != utility:
                retrieved_utility.utility = utility
                updated = True

            if updated:
                retrieved_utility.updateAt = datetime.now(timezone.utc)
                sess.commit()
            return updated
        except (NoResultFound, DataError, TypeError):
            raise UtilityNotFoundException()

    @staticmethod
    def get_utility(offer_id: str, sess: Session) -> UtilitySchema:
        """
        Retrieves utility from the database
        Args:
            offer_id:
            sess:

        Returns:

        """
        retrieved_utility: Utility = sess.execute(
            select(Utility).where(Utility.id == offer_id)
        ).scalar_one()

        return UtilitySchema(
            offer_id=retrieved_utility.offer_id,
            utility=retrieved_utility.utility,
            createdAt=retrieved_utility.createdAt,
            updateAt=retrieved_utility.updateAt
        )
