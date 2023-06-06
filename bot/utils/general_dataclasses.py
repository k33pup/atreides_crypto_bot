from dataclasses import dataclass


@dataclass
class Signal:
    coin: str
    type: str
    probability: int
