from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def get_possible_moves(self):
        pass
