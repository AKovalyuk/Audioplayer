"""Module with classes for cycled linked list"""

from typing import Any, Iterable, List, Optional
NoneType = type(None)


class LinkedListItem:
    """Class for cycled LinkedList node"""
    def __init__(self, value: Any, next_=None, previous=None) -> None:
        """
        Constructor for LinkedListItem
        :param value: data inside node
        :param next_: next node
        :param previous: previous node
        """
        if not isinstance(next_, (NoneType, LinkedListItem)) or not isinstance(previous, (NoneType, LinkedListItem)):
            raise TypeError
        self.value = value
        self._next = next_
        self._previous = previous

    @property
    def next_item(self) -> Optional['LinkedListItem']:
        """Property getter for next node"""
        return self._next

    @property
    def previous_item(self) -> Optional['LinkedListItem']:
        """Property getter for previous node"""
        return self._previous

    @next_item.setter
    def next_item(self, new: Optional['LinkedListItem']) -> None:
        """
        Property setter for next node
        :param new: new next node
        """
        if not isinstance(new, (NoneType, LinkedListItem)):
            raise TypeError
        self._next = new

    @previous_item.setter
    def previous_item(self, new: Optional['LinkedListItem']) -> None:
        """
        Property setter for previous node
        :param new: new previous node
        """
        if not isinstance(new, (NoneType, LinkedListItem)):
            raise TypeError
        self._previous = new

class LinkedList:
    """Class, represents cycled LinkedList"""
    def __init__(self, initialisator=None) -> None:
        """
        Constructor for LinkedList
        :param initialisator: initialisator list
        """
        self.first_item = None
        self.length = 0
        if not initialisator is None:
            for item in initialisator:
                self.append(item)

    def append_left(self, value: Any) -> None:
        """
        Append element at end of list
        :param value: appended value
        """
        if self.first_item is None:
            self.first_item = LinkedListItem(value)
            self.first_item.previous_item = self.first_item
            self.first_item.next_item = self.first_item
        else:
            new_element = LinkedListItem(value, self.first_item, self.first_item.previous_item)
            self.first_item.previous_item = new_element
            new_element.previous_item.next_item = new_element
            self.first_item = new_element
        self.length += 1

    def append_right(self, value: Any) -> None:
        """
        Append element at start of list
        :param value: appended value
        """
        if self.first_item is None:
            self.first_item = LinkedListItem(value)
            self.first_item.previous_item = self.first_item
            self.first_item.next_item = self.first_item
        else:
            new_element = LinkedListItem(value, self.first_item, self.first_item.previous_item)
            self.first_item.previous_item = new_element
            new_element.previous_item.next_item = new_element
        self.length += 1

    append = append_right

    def remove(self, value: Any) -> None:
        """
        Remove element from list by value
        :param value: value to remove
        """
        if self.first_item is None:
            raise ValueError
        element = self.first_item
        for i in range(self.length):
            if element.value == value:
                break
            element = element.next_item
        if element.value != value:
            raise ValueError
        if i == 0:
            self.first_item = self.first_item.next_item
        element.previous_item.next_item = element.next_item
        element.next_item.previous_item = element.previous_item
        self.length -= 1
        if len(self) == 0:
            self.first_item = None

    def insert(self, index: int, value: Any) -> None:
        """
        Insert new element after previous node
        :param index: position
        :param value: inserted value
        """
        if not isinstance(index, int):
            raise TypeError
        if index < 0:
            raise IndexError
        if index == 0:
            self.append_left(value)
            return
        previous = self.first_item
        for _ in range(index):
            previous = previous.next_item
        previous = previous.previous_item
        new_element = LinkedListItem(value, previous.next_item, previous)
        previous.next_item = new_element
        new_element.next_item.previous_item = new_element
        self.length += 1

    @property
    def last(self) -> LinkedListItem:
        """Property getter last element"""
        if self.first_item is None:
            return None
        return self.first_item.previous_item.value

    def __len__(self) -> int:
        return self.length

    def __contains__(self, value: Any) -> bool:
        """
        Special method for operator in
        :param value: target value
        """
        if self.length == 0:
            return False
        element = self.first_item
        for _ in range(self.length):
            if value == element.value:
                break
            element = element.next_item
        return element.value == value

    def __iter__(self) -> 'LinkedListIterator':
        return LinkedListIterator(self)

    def __reversed__(self) -> 'LinkedListReversed':
        return LinkedListReversed(self)

    def __getitem__(self, index: int) -> Any:
        """
        Method for supporting indexing
        :param index: index inside []
        """
        if not isinstance(index, int):
            raise TypeError
        if 0 <= index < self.length:
            element = self.first_item
            for _ in range(index):
                element = element.next_item
            return element.value
        raise IndexError

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Method for supporting indexing
        :param index: index inside []
        :param value: value to set
        """
        if not isinstance(index, int):
            raise TypeError
        if 0 <= index < self.length:
            element = self.first_item
            for _ in range(index):
                element = element.next_item
            element.value = value
        raise TypeError

    def __eq__(self, other: Iterable) -> bool:
        """
        Compare list with other sequence
        :param other: other sequence
        """
        if self.length != len(other):
            return False
        for first, second in zip(self, other):
            if first != second:
                return False
        return True

    def __str__(self) -> str:
        return f'<{", ".join([str(x) for x in self])}>'

    __repr__ = __str__

    def remove_by_index(self, index: int) -> None:
        """
        Method removes item by index
        :param index: target index
        """
        if not isinstance(index, int):
            raise TypeError
        if not 0 <= index < self.length:
            raise IndexError
        element = self.first_item
        for _ in range(index):
            element = element.next_item
        element.previous_item.next_item = element.next_item
        element.next_item.previous_item = element.previous_item
        if index == 0:
            self.first_item = self.first_item.next_item
        self.length -= 1
        if len(self) == 0:
            self.first_item = None


class LinkedListIterator:
    """Iterator for LinkedList class"""
    def __init__(self, linked_list: LinkedList) -> None:
        """
        Constructor for Linked List Iterator
        :param linked_list: linked list for iterations
        """
        if not isinstance(linked_list, LinkedList):
            raise TypeError
        self.element = linked_list.first_item
        self.linked_list = linked_list
        self.index = 0

    def __next__(self) -> Any:
        if self.index >= self.linked_list.length:
            raise StopIteration
        value = self.element.value
        self.element = self.element.next_item
        self.index += 1
        return value


class LinkedListReversed:
    """Reversed LinkedList object"""
    def __init__(self, linked_list: LinkedList) -> None:
        if not isinstance(linked_list, LinkedList):
            raise TypeError
        self.linked_list = linked_list

    def __iter__(self) -> 'LinkedListReversedIterator':
        return LinkedListReversedIterator(self.linked_list)


class LinkedListReversedIterator:
    """Iterator fo reversed LinkedList"""
    def __init__(self, linked_list: LinkedList) -> None:
        """
        Constructor for LinkedListReversedIterator
        :param linked_list: target list
        """
        if not isinstance(linked_list, LinkedList):
            raise TypeError
        if len(linked_list) == 0:
            self.index = -1
        else:
            self.element = linked_list.first_item.previous_item
            self.linked_list = linked_list
            self.index = len(linked_list) - 1

    def __next__(self) -> Any:
        if self.index < 0:
            raise StopIteration
        value = self.element.value
        self.element = self.element.previous_item
        self.index -= 1
        return value
