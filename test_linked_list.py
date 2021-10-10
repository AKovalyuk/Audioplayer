"""Tests for linked list"""

from linked_list import LinkedList
from pytest import mark, raises

def create_list(iterable):
    lst = LinkedList()
    for element in iterable:
        lst.append(element)
    return lst

@mark.parametrize('input,result', [
    ([1, 2, 3], [1, 2, 3]),
    ([], []),
    ([10], [10]),
])
def test_init(input, result):
    assert create_list(input) == result

@mark.parametrize('input,result', [
    ([1, 2, 3], [3, 2, 1]),
    ([], []),
    ([1, 2], [2, 1]),
    ([1], [1])
])
def test_left_append(input, result):
    lst = LinkedList()
    for i in input:
        lst.append_left(i)
    assert lst == result

@mark.parametrize('input, last', [
    ([1, 2, 3], 3), 
    ([1], 1),
    ([], None)
])
def test_last(input, last):
    assert create_list(input).last == last

@mark.parametrize('input, length', [
    ([1, 2, 3], 3), 
    ([1], 1),
    ([], 0)
])
def test_len(input, length):
    assert len(create_list(input)) == length

@mark.parametrize('input, element, result', [
    ([1, 2, 3], 3, True), 
    ([1], 1, True),
    ([], 0, False),
    ([], None, False),
    ([1, 2, 3], 0, False)
])
def test_contains(input, element, result):
    return result == (element in create_list(input))

@mark.parametrize('input, index, result', [
    ([1, 2, 3], 0, 1),
    ([1, 2, 3], 1, 2),
    ([1, 2, 3], 2, 3),
    ([0], 0, 0)
])
def test_getitem(input, index, result):
    assert create_list(input)[index] == result

@mark.parametrize('input, index', [
    ([1, 2, 3], -1),
    ([1, 2, 3], 6),
    ([1, 2, 3], 3),
    ([], 0)
])
def test_error_getitem(input, index):
    with raises(IndexError):
        create_list(input)[index]

@mark.parametrize('input, value, result', [
    ([1, 2, 3], 1, [2, 3]),
    ([1, 2, 3], 2, [1, 3]),
    ([1, 2, 3], 3, [1, 2]),
    ([1, 2, 3, 4, 5, 6], 1, [2, 3, 4, 5, 6]),
    ([0], 0, []),
    ([1, 2], 1, [2])
])
def test_remove(input, value, result):
    lst = create_list(input)
    lst.remove(value)
    assert lst == result

@mark.parametrize('input, value, result', [
    ([1, 2, 3], 0, [0, 1, 2, 3]),
    ([], 0, [0])
])
def test_left_append(input, value, result):
    lst = create_list(input)
    lst.append_left(value)
    assert result == lst

@mark.parametrize('input, value, index, result', [
    ([1, 2, 3], 0, 0, [0, 1, 2, 3]),
    ([1, 2, 3], 0, 1, [1, 0, 2, 3]),
    ([1, 2, 3], 0, 2, [1, 2, 0, 3]),
    ([1, 2, 3], 0, 3, [1, 2, 3, 0]),
    ([], 0, 0, [0])
])
def test_insert(input, value, index, result):
    lst = create_list(input)
    lst.insert(index, value)
    assert lst == result

@mark.parametrize('input, result', [
    ([1, 2, 3], [3, 2, 1]),
    ([], []),
    ([1], [1]),
    ([1, 2, 3, 4], [4, 3, 2, 1])
])
def test_reverse(input, result):
    assert list(reversed(create_list(input))) == result

@mark.parametrize('input, index, result', [
    ([1, 2, 3], 0, [2, 3]),
    ([1, 2, 3], 1, [1, 3]),
    ([1, 2, 3], 2, [1, 2]),
    ([0], 0, [])
])
def test_remove_by_index(input, index, result):
    lst = create_list(input)
    lst.remove_by_index(index)
    assert result == lst
