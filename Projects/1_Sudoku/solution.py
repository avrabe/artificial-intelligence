import copy
import sys

from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

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
    # TODO: Implement this function!
    raise NotImplementedError


def getPeers(box):
    already = {box: box}
    foo = "123456789"
    baba = "ABCDEFGHI"
    bar = box[1]
    boo = box[0]
    for i in foo:
        bbox = boo + i
        if (bbox not in already):
            yield (bbox)
        already[bbox] = bbox
    for i in baba:
        bbox = i + bar
        if (bbox not in already):
            yield (bbox)
        already[bbox] = bbox
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    for i in square_units:
        if box in i:
            for bbox in i:
                if (bbox not in already):
                    yield (bbox)
        already[bbox] = bbox
    # print("### ", box)
    pass

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for key, value in values.items():
        if (len(value) == 1):
            for i in getPeers(key):
                values[i] = values[i].replace(value, '')
                # print(i)

    return values


def cross(a, b):
    return [s + t for s in a for t in b]


def getRows(box):
    already = {box: box}
    foo = "123456789"
    baba = "ABCDEFGHI"
    bar = box[1]
    boo = box[0]
    for i in foo:
        bbox = boo + i
        if (bbox not in already):
            yield (bbox)
        already[bbox] = bbox


def getColumns(box):
    already = {box: box}
    foo = "123456789"
    baba = "ABCDEFGHI"
    bar = box[1]
    boo = box[0]
    for i in baba:
        bbox = i + bar
        if (bbox not in already):
            # print(bbox)
            yield (bbox)
        already[bbox] = bbox


def getSquare(box):
    already = {box: box}
    foo = "123456789"
    baba = "ABCDEFGHI"
    bar = box[1]
    boo = box[0]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    for i in square_units:
        if box in i:
            for bbox in i:
                if (bbox not in already):
                    yield (bbox)
            already[bbox] = bbox


def containsValue(value, peers, bvalues, key):
    concat = ""
    for i in peers:
        concat = concat + bvalues[i]
    # print(concat, key, value)
    return value not in concat


def only_choice(bvalues):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for key, values in bvalues.items():
        if (len(values) > 1):
            for value in values:
                if (containsValue(value, getPeers(key), bvalues, key)):
                    bvalues[key] = value
                if (containsValue(value, getRows(key), bvalues, key)):
                    bvalues[key] = value
                if (containsValue(value, getColumns(key), bvalues, key)):
                    bvalues[key] = value
                if (containsValue(value, getSquare(key), bvalues, key)):
                    bvalues[key] = value
                    # print("replace",key,values,value)

    return bvalues


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)

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

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    copy_values = copy.deepcopy(values)
    # print(iteration, "b")
    # display(copy_values)
    copy_values = reduce_puzzle(copy_values)
    if copy_values is False:
        return False  ## Failed earlier
    # print(iteration, "a")
    # display(copy_values)
    # for x in copy_values:
    #    print (x, copy_values[x])

    # Choose one of the unfilled squares with the fewest possibilities
    found_key = "A1"
    found_values = ""
    length = sys.maxsize
    solved = True

    for key, value in copy_values.items():
        if (len(value) > 1):
            solved = False

    if solved:
        # print(iteration, "found")
        return copy_values

    for key, value in copy_values.items():
        if (len(value) == 1):
            solved = True
        else:
            solved = False
        if (len(value) < length and len(value) > 1):
            length = len(value)
            found_values = copy_values[key]
            found_key = key

    for value in found_values:
        # print(iteration,found_key, value, found_values)
        copy_copy_values = copy.deepcopy(values)
        copy_copy_values[found_key] = value
        # print(iteration, "search")
        # display(copy_copy_values)
        ret = search(copy_copy_values, iteration + 1)
        if ret:
            # print(iteration, "found")
            return ret

    # print(iteration,"not found", found_key, found_values)
    return False
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    # If you're stuck, see the solution.py tab!


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
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
