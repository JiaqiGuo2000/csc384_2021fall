from constraints import *
from backtracking import bt_search, GacEnforce
from csp import Variable, CSP
from csp_problems import nQueens, sudokuCSP, solve_planes
from sudoku import b1, b5, b6
from plane_scheduling import p1, p2, p3, p4, p5, p6, p7, check_plane_solution
import argparse
import time
import signal

v1 = Variable('V1', [1, 2])
v2 = Variable('V2', [1, 2])
v3 = Variable('V3', [1, 2, 3, 4, 5])
v4 = Variable('V4', [1, 2, 3, 4, 5])
v5 = Variable('V5', [1, 2, 3, 4, 5])
v6 = Variable('V6', [1, 3, 4, 5])
v7 = Variable('V7', [1, 3, 4, 5])
ac1 = AllDiffConstraint('1', [v1,v2,v3])
ac2 = AllDiffConstraint('1', [v1,v2,v4])
ac3 = AllDiffConstraint('1', [v1,v2,v5])
ac4 = AllDiffConstraint('1', [v3,v4,v5,v6])
ac5 = AllDiffConstraint('1', [v3,v4,v5,v7])
vars = [v1, v2, v3, v4, v5, v6, v7]
cnstrs = [ac1,ac2,ac3,ac4,ac5]
testcsp = CSP('test2', vars, cnstrs)
GacEnforce(cnstrs, testcsp, None, None)

v1 = Variable('V1', [1, 2])
v2 = Variable('V2', [1, 2])
v3 = Variable('V3', [1, 2, 3, 4, 5])
v4 = Variable('V4', [1, 2, 3, 4, 5])
v5 = Variable('V5', [1, 2, 3, 4, 5])
v6 = Variable('V6', [1, 3, 4, 5])
v7 = Variable('V7', [1, 3, 4, 5])
ac1 = AllDiffConstraint('1', [v1, v2, v3])
ac2 = AllDiffConstraint('1', [v1, v2, v4])
ac3 = AllDiffConstraint('1', [v1, v2, v5])
ac4 = AllDiffConstraint('1', [v3, v4, v5, v6])
ac5 = AllDiffConstraint('1', [v3, v4, v5, v7])
neq = NeqConstraint('2', [v6, v7])
vars = [v1, v2, v3, v4, v5, v6, v7]
cnstrs = [ac1, ac2, ac3, ac4, ac5, neq]
testcsp = CSP('test2', vars, cnstrs)
val = GacEnforce(cnstrs, testcsp, None, None)


def main():
    pre_ret = [[['AC-1','AC01', 'AC02', 'AC03', 'AC04', 'AC05']]]
    for solution in pre_ret:
        accept = True
        for plane in solution:
            if len(plane) == 1:
                continue
            curr_distance = 0
            print(plane[1:])
            for flight in plane[1:]:
                if flight in ['AC03']:
                    curr_distance = 0
                else:
                    curr_distance += 1
                print(curr_distance)
                if curr_distance >= 2:
                    accept = False

                    break

main()