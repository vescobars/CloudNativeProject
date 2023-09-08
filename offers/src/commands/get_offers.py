from .base_command import BaseCommannd
from ..models.offer import Offer, OfferDefailtSchema
from ..session import Session
from ..errors.errors import InvalidParam, IncompleteParams
from datetime import datetime
import uuid


class GetOffers(BaseCommannd):
    def __init__(self, data, userId=None):
        if 'post' in data:
            if self.is_uuid(data['post']):
                self.postId = data['post']
            else:
                raise InvalidParam()
        else:
            self.postId = None

        if 'owner' in data:
            if data['owner'] == 'me':
                self.owner = userId
            else:
                self.owner = data['owner']
        else:
            self.owner = None

    def execute(self):
        session = Session()
        offers = session.query(Offer).all()

        if self.postId != None:
            offers = [offer for offer in offers if offer.postId ==
                      uuid.UUID(self.postId)]

        if self.owner != None:
            offers = [offer for offer in offers if offer.userId ==
                      uuid.UUID(self.owner)]

        offers = OfferDefailtSchema(many=True).dump(offers)
        session.close()
        return offers
