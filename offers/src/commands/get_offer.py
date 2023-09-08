from .base_command import BaseCommannd
from ..models.offer import Offer, OfferDefailtSchema
from ..session import Session
from ..errors.errors import InvalidParam, OfferNotFoundError
from datetime import datetime


class GetOffer(BaseCommannd):
    def __init__(self, offer_id):
        if self.is_uuid(offer_id):
            self.offer_id = offer_id
        else:
            raise InvalidParam()

    def execute(self):
        session = Session()
        if len(session.query(Offer).filter_by(id=self.offer_id).all()) <= 0:
            session.close()
            raise OfferNotFoundError()

        offer = session.query(Offer).filter_by(id=self.offer_id).one()
        schema = OfferDefailtSchema()
        offer = schema.dump(offer)
        session.close()
        return offer
