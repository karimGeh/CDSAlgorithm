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

example = [
    [5, 2, 3, 6, 7],  # machine 1
    [2, 4, 4, 5, 3],  # machine 2
    [3, 2, 5, 4, 2],  # machine 3
]

example_CDS = CDS(example)


#show chart 
GanttDiagram(example_CDS).showChart()

