class PhysicalDistributionBase:
    def ship(self, baggage: "Baggage") -> "Baggage":
        return Baggage()

    def receive(self, baaggage: "Baggage"):
        pass


class Baggage:
    pass


class TransportService:
    """輸送を執り行うドメインサービス"""

    def ransport(
        self,
        base_from: "PhysicalDistributionBase",
        base_to: "PhysicalDistributionBase",
        baggage: "Baggage",
    ):
        shipped_baggage = base_from.ship(baggage)
        base_to.receive(shipped_baggage)
