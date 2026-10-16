from dataclasses import dataclass


@dataclass
class Driver:
    driverId: int
    forename: str
    surname: str
    nationality: str
    podi: int = 0

    def __hash__(self):
        return hash(self.driverId)

    def __eq__(self, other):
        return self.driverId == other.driverId

    def __str__(self):
        return f"{self.forename} {self.surname}"