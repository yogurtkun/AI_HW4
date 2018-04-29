#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys,time

ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in range(9):
        row = ''
        for j in range(9):
            row += (str(board[i*9 + j]) + " ")
        print(row)


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    result = backtracking(board)
    # print(result)  # TODO: Comment out prints when timing runs.
    # print()

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result


def index2tuple(index):
    return (int(index / 9), index % 9)


def tuple2index(tuple):
    return tuple[0] * 9 + tuple[1]


def topleft_tuple(t):
    r, c = t
    r = int(r / 3) * 3
    c = int(c / 3) * 3
    return (r, c)


all_set = set([str(x) for x in range(1,10)])
def remaining_values(index, board):
    if board[index] != '0':
        return (index, set())

    tuple_pos = index2tuple(index)
    data_set = set()

    for i in range(9):
        data_set.add(board[tuple2index((tuple_pos[0], i))])
        data_set.add(board[tuple2index((i, tuple_pos[1]))])

    tl_tuple = topleft_tuple(tuple_pos)

    for i in range(tl_tuple[0], tl_tuple[0] + 3):
        for j in range(tl_tuple[1], tl_tuple[1] + 3):
            data_set.add(board[tuple2index((i, j))])

    return (index, all_set - data_set)


def list_copy(remaining_list):
    new_list = []

    for item in remaining_list:
        new_list.append((item[0], item[1].copy()))

    return new_list


def change_order(try_set):
    return list(try_set)


def change_remaining_list(remaining_list, index, new_ele):
    relate_set = set()

    new_remaining_list = []

    tuple = index2tuple(index)

    for i in range(9):
        relate_set.add(tuple2index((tuple[0],i)))
        relate_set.add(tuple2index((i,tuple[1])))

    tl_tuple = topleft_tuple(tuple)

    for i in range(tl_tuple[0], tl_tuple[0] + 3):
        for j in range(tl_tuple[1], tl_tuple[1] + 3):
            relate_set.add(tuple2index((i, j)))

    for item in remaining_list:
        if item[0] == index:
            continue
        elif item[0] in relate_set:
            new_remaining_list.append((item[0], item[1]-set([new_ele])))
        else:
            new_remaining_list.append((item[0], item[1].copy()))

    return new_remaining_list


def solve_board(board, remaining_list):
    if len(remaining_list) == 0:
        return board

    try_index, try_set = min(remaining_list, key=lambda x: len(x[1]))
    if len(try_set) == 0:
        return None

    try_list = change_order(try_set)

    for new_ele in try_list:
        new_board = board.copy()
        new_board[try_index] = new_ele
        new_remaining_list = change_remaining_list(remaining_list, try_index, new_ele)

        # _t = index2tuple(try_index)
        # print("Change (%d,%d) to %s:"%(_t[0],_t[1],new_ele))
        # print_board(new_board)

        res_board = solve_board(new_board,new_remaining_list)

        if res_board is not None:
            return res_board

    return None


def backtracking(board):
    """Takes a board and returns solved board."""
    start_time = time.time()

    remaining_list = [remaining_values(i, board) for i in range(len(board))]
    remaining_list = list(filter(lambda x: len(x[1]) != 0, remaining_list))

    board = list(board)
    solved_board = solve_board(board, remaining_list)
    solved_board = ''.join(solved_board)

    take_time = time.time() - start_time

    print("It spend %.4f seconds"%(take_time,))

    return solved_board


if __name__ == '__main__':

    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = sys.argv[1]
        write_solved(board)

    else:
        print("Running all from sudokus_start")

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = line
            # print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')

        print("Finished all boards in file.")
