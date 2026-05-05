from dataclasses import dataclass, asdict, field
from datetime import datetime
from bson import ObjectId

@dataclass
class BookingModel:
    service_id: str
    service_title: str
    customer_id: str
    customer_name: str
    provider_id: str
    scheduled_date: datetime
    status: str = "pending" # pending, accepted, rejected, completed, cancelled
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = None

    def to_dict(self):
        d = asdict(self)
        if self._id:
            d["_id"] = self._id
        else:
            d.pop("_id", None)
        return d

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        _id = data.pop("_id", None)
        return cls(_id=_id, **data)
