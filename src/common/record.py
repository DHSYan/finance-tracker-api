from typing import Dict, Any

class Record:
    def __init__(self, amount: float, description: str, record_id: str = None):
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number.")
        if not isinstance(description, str) or not description:
            raise ValueError("Description must be a non-empty string.")

        self.amount = amount
        self.description = description
        self.record_id = record_id

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Record object to a dictionary."""        return {
            "record_id": self.record_id,
            "amount": self.amount,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":
        """Creates a Record object from a dictionary."""        return cls(
            amount=data.get("amount"),
            description=data.get("description"),
            record_id=data.get("record_id"),
        )
