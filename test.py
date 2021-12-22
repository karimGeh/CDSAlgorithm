"""
  Created by :  Karim Gehad
  On         :  13/11/2021

  email      :  karimgehad@outlook.com
  github     :  https://github.com/karimGeh
  linkedIn   :  https://www.linkedin.com/in/karim-gehad
"""
# if "CDS" not in dir():
from classes.CDS import CDS
from classes.GanttDiagram import GanttDiagram

# examples


# normal test
# example = [
#     [5, 2, 3, 6, 7],  # machine 1
#     [2, 4, 4, 5, 3],  # machine 2
#     [3, 2, 5, 4, 2],  # machine 3
# ]

# test with delay Array
# example = [
#     [5, 2, 3, 6, 7],  # machine 1
#     [1, 4, 4, 5, 2],  # machine 2
# ]

# delayArray = [7, 9, 10, 15, 4]
# example_CDS = CDS(example)


# # show chart
# GanttDiagram(
#     example_CDS,
#     method="delay",
# ).showChart()


# test with preparation
example = [
    # 0  1  2  3  4
    [5, 5, 3, 6, 7],  # machine 1
    [2, 4, 5, 5, 3],  # machine 2
    [3, 2, 5, 4, 2],  # machine 3
]

delayArray = [10, 15, 12, 8, 13]

preparation_matrix = [
    [
        [2, 2, 3, 2, 1],
        [2, 3, 2, 3, 3],
        [3, 2, 3, 4, 2],
        [1, 3, 2, 3, 2],
        [3, 4, 2, 3, 1],
    ],
    [
        [3, 1, 3, 2, 1],
        [3, 3, 2, 3, 3],
        [3, 2, 3, 4, 2],
        [2, 1, 2, 4, 2],
        [2, 3, 2, 3, 2],
    ],
    [
        [2, 3, 1, 2, 3],
        [1, 2, 3, 3, 3],
        [4, 3, 2, 3, 1],
        [3, 2, 2, 1, 2],
        [3, 2, 3, 4, 2],
    ],
]

example_CDS = CDS(example, preparation_matrix=preparation_matrix, delayArray=delayArray)

bestSeq = example_CDS.get_solution_with_delay_and_preparation()


print(bestSeq)

GanttDiagram(
    example_CDS,
    method="preparation",
).showChart()
