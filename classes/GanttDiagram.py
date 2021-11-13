"""
  Created by :  Karim Gehad
  On         :  13/11/2021

  email      :  karimgehad@outlook.com
  github     :  https://github.com/karimGeh
  linkedIn   :  https://www.linkedin.com/in/karim-gehad
"""
import sys, os
sys.path.append(os.path.dirname(__file__))
from CDS import CDS
import matplotlib.pyplot as plt

class GanttDiagram:
    def __init__(self,CDSObject: CDS, sequence: list[int] = None) -> None:
        self.jobsMatrix = CDSObject.jobsMatrix
        self.solutionMatrix = CDSObject.getSolutionAsMatrix(sequence)
        if not sequence : sequence = CDSObject.get_CDS_solution()["sequence"]
        self.sequence = sequence

    def getJobMetaData(self, jobIndex: int, machineIndex: int) -> dict:
        return {
            "timeOnMachine": self.jobsMatrix[machineIndex][jobIndex],
            "startTime": self.solutionMatrix[jobIndex][machineIndex] - self.jobsMatrix[machineIndex][jobIndex],
            "finishTime": self.solutionMatrix[jobIndex][machineIndex],
        }

    def generateNrandomColors(self,n:int)->list[str]:
      f=plt.cm.get_cmap("hsv", n)
      return [f(i) for i in range(n)]

    def showChart(self):
        colors = self.generateNrandomColors(len(self.solutionMatrix))

        _, ax = plt.subplots(1, figsize=(10,2))

        y = []
        x = []
        startTime = []
        for machineIndex in range(len(self.jobsMatrix)):
          jobs = self.sequence
          timeOnFirstMachine =  [self.getJobMetaData(i,machineIndex)["timeOnMachine"] for i in jobs]
          startTimeOnFirstMachine =  [self.getJobMetaData(i,machineIndex)["startTime"] for i in jobs]
          y =  [len(self.jobsMatrix) - machineIndex]*len(jobs) + y 
          x = timeOnFirstMachine + x 
          startTime = startTimeOnFirstMachine + startTime 

        ax.barh(
          y,
          x, 
          left =startTime, 
          color=colors,
        )
        plt.show()
