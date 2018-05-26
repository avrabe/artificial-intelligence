import copy
import itertools
import sys

from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonals1 = [[r + c for r, c in itertools.zip_longest(rows, cols)]]
diagonals2 = [[r + c for r, c in itertools.zip_longest(rows[::-1], cols)]]

unitlist = row_units + column_units + square_units + diagonals1 + diagonals2

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    :param dict values: a dictionary of the form {'box_name': '123456789', ...}
    :returns: dict. The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    for box in peers.keys():
        digits = values[box]
        for unit in units[box]:
            foo = [b for b in unit if digits == values[b] and len(digits) == 2]
            if len(foo) == 2:
                for digit in digits:
                    for peer in unit:
                        if peer not in foo and digit in values[peer]:
                            values[peer] = values[peer].replace(digit, '')
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    :param dict values: a dictionary of the form {'box_name': '123456789', ...}
    :returns: dict. The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    :param dict values: a dictionary of the form {'box_name': '123456789', ...}
    :returns: dict.

    Returns The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies
    :param dict values: a dictionary of the form {'box_name': '123456789', ...}
    :return: dict or False

    Returns the values dictionary after continued application of the constraint strategies no longer produces any changes,
    or False if the puzzle is unsolvable.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        only_choice(values)
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    :param dict values: a dictionary of the form {'box_name': '123456789', ...}
    :returns: dict or False. The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    copy_values = copy.deepcopy(values)
    copy_values = reduce_puzzle(copy_values)
    if copy_values is False:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    found_key = "A1"
    found_values = ""
    length = sys.maxsize
    solved = True

    for key, value in copy_values.items():
        if len(value) > 1:
            solved = False

    if solved:
        return copy_values

    for key, value in copy_values.items():
        if length > len(value) > 1:
            length = len(value)
            found_values = copy_values[key]
            found_key = key

    for value in found_values:
        copy_copy_values = copy.deepcopy(values)
        copy_copy_values[found_key] = value
        ret = search(copy_copy_values)
        if ret:
            return ret

    return False
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    # If you're stuck, see the solution.py tab!


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    :param str grid: a string representing a sudoku grid.
    Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    :returns: dict or False. The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
