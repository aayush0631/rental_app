from dataclasses import dataclass, asdict, field
from datetime import datetime
from bson import ObjectId
from typing import List

@dataclass
class Location:
    type: str = "Point"
    coordinates: List[float] = field(default_factory=lambda: [0.0, 0.0]) # [longitude, latitude]

@dataclass
class ServiceModel:
    title: str
    description: str
    category: str
    price: float
    provider_id: str # User ObjectId string
    provider_name: str
    address: str = ""
    location: Location = field(default_factory=Location)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = None

    def to_dict(self):
        d = asdict(self)
        if self._id:
            d["_id"] = self._id
        else:
            d.pop("_id", None)
        # Ensure location is in GeoJSON format
        if isinstance(self.location, Location):
            d["location"] = asdict(self.location)
        return d

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        _id = data.pop("_id", None)
        loc_data = data.pop("location", None)
        if loc_data:
            location = Location(**loc_data)
        else:
            location = Location()
        return cls(_id=_id, location=location, **data)
