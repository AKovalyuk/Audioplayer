"""Module width Composition and PlayList classes"""

from typing import Optional
from linked_list import LinkedList

class Composition:
    """Class represents music composition"""
    def __init__(self, name) -> None:
        self.__name = name

    def play(self) -> str:
        """Get name of mp3 file"""
        return self.__name

    @property
    def name(self) -> str:
        """Property for composition's name"""
        return self.__name


class PlayList:
    """Playlist contains compositions"""
    def __init__(self, name: str) -> None:
        self.container = LinkedList()
        self.name = name
        self.current_composition = None
        self.current_index = -1

    def append(self, composition: Composition) -> None:
        """Add composition in playlist"""
        self.container.append(composition)

    def remove(self, index: int) -> None:
        """Remove composition from playlist"""
        if 0 <= index < len(self.container):
            if index == self.current_index:
                self.current_index = -1
                self.current_composition = None
            self.container.remove_by_index(index)

    def push_forward(self, index: int) -> None:
        """Push composition forwards"""
        if 0 <= index < len(self.container):
            new_index = (index - 1) % self.container.length
            if len(self.container) != 1:
                self.container[index], self.container[new_index] = self.container[new_index], self.container[index]
            if index == self.current_index:
                self.current_index = new_index
            elif new_index == self.current_index:
                self.current_index = index

    def push_back(self, index: int) -> None:
        """Push composition backwards"""
        if 0 <= index < len(self.container):
            new_index = (index + 1) % self.container.length
            if len(self.container) != 1:
                self.container[index], self.container[new_index] = self.container[new_index], self.container[index]
            if index == self.current_index:
                self.current_index = new_index
            elif new_index == self.current_index:
                self.current_index = index

    def current(self) -> Optional[str]:
        """Return current composition"""
        if self.current_composition is None:
            return None
        return self.current_composition.play()

    def next(self) -> None:
        """Go to next composition"""
        if self.current_composition is None:
            return
        self.current_index = (self.current_index + 1) % len(self.container)
        self.current_composition = self.container[self.current_index]

    def prev(self) -> None:
        """Go to previous composition"""
        if self.current_composition is None:
            return
        self.current_index = (self.current_index - 1) % len(self.container)
        self.current_composition = self.container[self.current_index]

    def get_data(self) -> dict:
        """Return playlist data"""
        return {
            'name': self.name,
            'current_index': self.current_index,
            'compositions': [composition.name for composition in self.container]
        }

    def play(self, index: int) -> None:
        """Return current composition"""
        element = self.container.first_item
        for _ in range(index):
            element = element.next_item
        self.current_index = index
        self.current_composition = element.value
