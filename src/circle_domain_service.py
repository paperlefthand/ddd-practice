from circle import Circle
from icircle_repository import ICircleRepository


class CircleDomainService:
    def __init__(self, circle_repository: ICircleRepository):
        self.circle_repository = circle_repository

    def exists(self, circle: Circle):
        """サークルの重複判定
        - 重複判定の詳細なロジックをこのメソッドに記載
        """
        found = self.circle_repository.find_by_name(circle.name)
        return found is not None

    # def create_circle(self, circle: Circle):
    #     self.__circle_repository.create_circle(circle)

    # def find_circle(self, circle_id: str):
    #     return self.__circle_repository.find_circle(circle_id)
