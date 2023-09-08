from .base_command import BaseCommannd
from ..models.offer import Offer, OfferSchema, CreatedOfferSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidParamFormat
from datetime import datetime
from marshmallow import exceptions

class CreateOffer(BaseCommannd):
    def __init__(self, data, userId=None):
        self.data = data
        if userId != None:
            self.data['userId'] = userId

    def execute(self):
        try:
            posted_offer = OfferSchema(
                only=(
                    'postId', 'userId', 'description',
                    'size', 'fragile', 'offer'
                )
            ).load(self.data)
            offer = Offer(**posted_offer)

            if not self.valid_size() or not self.valid_offer():
                raise InvalidParamFormat()

            session = Session()

            session.add(offer)
            session.commit()

            new_offer = CreatedOfferSchema().dump(offer)
            session.close()

            return new_offer
        except (TypeError, exceptions.ValidationError):
            raise IncompleteParams

    def valid_size(self):
        size = self.data['size'].upper()
        return size == 'LARGE' or size == 'MEDIUM' or size == 'SMALL'

    def valid_offer(self):
        offer = self.data['offer']
        return offer >= 0
