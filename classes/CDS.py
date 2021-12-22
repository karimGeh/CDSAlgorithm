"""
  Created by :  Karim Gehad
  On         :  13/11/2021

  email      :  karimgehad@outlook.com
  github     :  https://github.com/karimGeh
  linkedIn   :  https://www.linkedin.com/in/karim-gehad
"""
from itertools import permutations
from typing import Sequence


class CDS:
    def __init__(
        self,
        jobsMatrix: list[list[int]],
        delayArray: list[int] = [],
        preparation_matrix: list[list[int]] = [],
    ) -> None:
        self.jobsMatrix = jobsMatrix
        self.numberOfMachines = len(jobsMatrix)
        self.numberOfJobs = len(jobsMatrix[0])
        self.delayArray = delayArray
        self.preparation = preparation_matrix

        if len(self.delayArray) and len(self.delayArray) != len(self.jobsMatrix[0]):
            raise RuntimeError("delay array must have the same length of jobs")

        if len(preparation_matrix):
            if len(preparation_matrix) != self.numberOfMachines or any(
                len(preparation_matrix[i]) != self.numberOfJobs
                for i in range(self.numberOfMachines)
            ):
                raise RuntimeError("cant run script")

    def generateTwoVirtualMachines(self, k: int) -> list[list[int]]:
        if not (1 <= k <= len(self.jobsMatrix) - 1):
            return [[], []]

        firstKMachines = zip(*self.jobsMatrix[0:k])
        lastKMachines = zip(*self.jobsMatrix[-k:])

        virtualMachineOne = [sum(v) for v in firstKMachines]
        virtualMachineTwo = [sum(v) for v in lastKMachines]

        return [virtualMachineOne, virtualMachineTwo]

    @staticmethod
    def getSigmaJohnson(MachineOne: list[int], MachineTwo: list[int]):
        jobs = [[i, j] for i, j in zip(MachineOne, MachineTwo)]

        U = [k for k, u in enumerate(jobs) if u[0] <= u[1]]
        V = [k for k, v in enumerate(jobs) if v[0] > v[1]]

        U = list(sorted(U, key=lambda k: MachineOne[k]))
        V = list(sorted(V, key=lambda k: MachineTwo[k], reverse=True))

        return U + V  # Sigma Johnson

    def get_C(self, jobIndex: int, machineIndex: int, sequence: list[int]) -> int:
        # this method is nothing but an implementation
        # of the mathematical model.

        if jobIndex == 0 and machineIndex == 0:
            return self.jobsMatrix[0][sequence[jobIndex]]

        if jobIndex == 0:
            return (
                self.get_C(0, machineIndex - 1, sequence)
                + self.jobsMatrix[machineIndex][sequence[jobIndex]]
            )

        if machineIndex == 0:
            return (
                self.get_C(jobIndex - 1, 0, sequence)
                + self.jobsMatrix[0][sequence[jobIndex]]
            )

        return (
            max(
                self.get_C(jobIndex - 1, machineIndex, sequence),
                self.get_C(jobIndex, machineIndex - 1, sequence),
            )
            + self.jobsMatrix[machineIndex][sequence[jobIndex]]
        )

    def getTimeOfJobInMachine(
        self, jobIndex: int, machineIndex: int, sequence: list[int]
    ) -> int:
        return self.jobsMatrix[machineIndex][sequence[jobIndex]]

    def getPreparationTimeOfJob(
        self, job_index, previous_job_index, machine_index, sequence
    ):
        # print(
        #     f"{sequence[job_index]=}",
        #     f"{sequence[previous_job_index]=}",
        #     f"{machine_index=}",
        #     f"=",
        #     self.preparation[machine_index][sequence[previous_job_index]][
        #         sequence[job_index]
        #     ],
        # )
        return self.preparation[machine_index][sequence[previous_job_index]][
            sequence[job_index]
        ]

    def get_C_with_preparation(
        self, jobIndex: int, machineIndex: int, sequence: list[int]
    ) -> int:
        if jobIndex == 0 and machineIndex == 0:
            return (
                self.getTimeOfJobInMachine(0, 0, sequence)
                # + 0
                + self.getPreparationTimeOfJob(0, 0, 0, sequence)
            )

        if jobIndex == 0:
            return (
                max(
                    self.get_C_with_preparation(0, machineIndex - 1, sequence),
                    self.getPreparationTimeOfJob(0, 0, machineIndex, sequence),
                )
                + self.getTimeOfJobInMachine(0, machineIndex, sequence)
            )

        if machineIndex == 0:
            return (
                self.get_C_with_preparation(jobIndex - 1, 0, sequence)
                + self.getPreparationTimeOfJob(jobIndex, jobIndex - 1, 0, sequence)
                + self.getTimeOfJobInMachine(jobIndex, 0, sequence)
            )

        return (
            max(
                self.get_C_with_preparation(jobIndex, machineIndex - 1, sequence),
                self.get_C_with_preparation(jobIndex - 1, machineIndex, sequence)
                + self.getPreparationTimeOfJob(
                    jobIndex, jobIndex - 1, machineIndex, sequence
                ),
            )
            + self.getTimeOfJobInMachine(jobIndex, machineIndex, sequence)
        )

    def get_C_max(self, sequence: list[int]) -> int:
        # getting C max is nothing but getting
        # when the last job will finish
        return self.get_C(
            len(self.jobsMatrix[0]) - 1,  # last job index
            len(self.jobsMatrix) - 1,  # last machine index
            sequence,
        )

    def get_C_max_with_preparation(self, sequence: list[int]):
        return self.get_C_with_preparation(
            len(self.jobsMatrix[0]) - 1,  # last job index
            len(self.jobsMatrix) - 1,  # last machine index
            sequence,
        )

    def get_sequence_with_proper_time(self):
        TP_list = [0 for i in "0" * self.numberOfJobs]
        defaultSequence = list(range(self.numberOfJobs))

        for i in range(self.numberOfJobs):
            TP_list[i] = sum(
                [
                    self.getTimeOfJobInMachine(i, k, defaultSequence)
                    + self.getPreparationTimeOfJob(i, i, k, defaultSequence)
                    for k in range(self.numberOfMachines)
                ]
            )

        listOfJobs = [{"index": i, "TP": TP_list[i]} for i in range(self.numberOfJobs)]

        bestSeq = [
            k["index"]
            for k in sorted(listOfJobs, key=lambda element: element["TP"], reverse=True)
        ]
        # print(bestSeq, sep="\n")

        return bestSeq

    def get_CDS_solution(self) -> dict:
        # this function simulate all possible k
        # and return the sequence with the lowest execution time

        #! initialize first value with k = 1
        # * generate two virtual machines
        optimalK = 1
        # * generate the johnsonsSequence
        optimalSequence = self.getSigmaJohnson(*self.generateTwoVirtualMachines(1))
        # * calculate C_max
        optimalTime = self.get_C_max(optimalSequence)

        #! iterate from k = 2 to k = m - 1 (where m is the number
        #! of machines we have) over jobsMatrix
        for k in range(2, len(self.jobsMatrix)):
            # * generate two virtual machines using a k
            vm1, vm2 = self.generateTwoVirtualMachines(k)

            # * generate the johnsonsSequence
            johnsonsSequence = self.getSigmaJohnson(vm1, vm2)

            # * calculate how much time it will take to to
            # * execute that sequence
            time = self.get_C_max(johnsonsSequence)

            if time < optimalTime:
                # if the above condition is true that means
                # we have found a new optimal solution
                optimalTime = time
                optimalK = k
                optimalSequence = johnsonsSequence

        return {"k": optimalK, "time": optimalTime, "sequence": optimalSequence}

    def get_solution_with_delay(self) -> dict:
        # this function simulate all possible k
        # and return the optimal sequence

        #! initialize the index of the last machine
        indexOfTheLastMachine = len(self.jobsMatrix) - 1

        #! initialize first/default solution with k = 1
        optimalK = 1
        ###* generate the johnsonsSequence
        optimalSequence = self.getSigmaJohnson(*self.generateTwoVirtualMachines(1))

        ###* calculate C_max
        TotalDelayTime = sum(
            max(
                0,
                self.get_C(k, indexOfTheLastMachine, optimalSequence) - d,
            )
            for k, d in enumerate(self.delayArray)
        )

        #! iterate from k = 2 to k = m - 1 (where m is the number
        #! of machines we have) over jobsMatrix
        for k in range(2, len(self.jobsMatrix)):
            # * generate two virtual machines using a k
            vm1, vm2 = self.generateTwoVirtualMachines(k)

            # * generate the johnsonsSequence
            johnsonsSequence = self.getSigmaJohnson(vm1, vm2)

            # * calculate TT
            newTotalDelayTime = sum(
                max(0, self.get_C(k, indexOfTheLastMachine, johnsonsSequence) - d)
                for k, d in enumerate(self.delayArray)
            )

            if newTotalDelayTime < TotalDelayTime:
                # if the above condition is true that means
                # we have found a new optimal solution
                TotalDelayTime = newTotalDelayTime
                optimalK = k
                optimalSequence = johnsonsSequence

        return {
            "k": optimalK,
            "time": self.get_C_max(optimalSequence),
            "sequence": optimalSequence,
            "TT": TotalDelayTime,
        }

    def get_solution_with_preparation(self) -> dict:
        # this function simulate all possible k
        # and return the sequence with the lowest execution time

        optimalSequence = self.get_sequence_with_proper_time()
        optimalTime = self.get_C_max_with_preparation(optimalSequence)

        # ! iterate from k = 2 to k = m - 1 (where m is the number
        # ! of machines we have) over jobsMatrix

        return {"k": 0, "time": optimalTime, "sequence": optimalSequence}

    def get_solution_with_delay_and_preparation(self) -> dict:
        # this function simulate all possible k
        # and return the sequence

        optimalSequence = self.get_sequence_with_proper_time()
        optimalTime = self.get_C_max_with_preparation(optimalSequence)

        TotalDelayTime = sum(
            max(
                0,
                self.get_C_with_preparation(
                    k, self.numberOfMachines - 1, optimalSequence
                )
                - d,
            )
            for k, d in enumerate(self.delayArray)
        )

        return {
            "k": 0,
            "time": optimalTime,
            "sequence": optimalSequence,
            "TT": TotalDelayTime,
        }

    def getSolutionAsMatrix(self, optimalSequence: list[int] = None, method="normal"):
        if not optimalSequence:
            optimalSequence = self.get_CDS_solution()["sequence"]

        # return [
        #     [
        #         self.get_C(jobIndex, machineIndex, optimalSequence) for jobIndex in range(len(optimalSequence))
        #     ] for machineIndex in range(len(self.jobsMatrix))
        # ]

        if method in ["normal", "delay"]:
            solution = [
                [
                    self.get_C(index, machineIndex, optimalSequence)
                    for machineIndex in range(len(self.jobsMatrix))
                ]
                for index, _ in enumerate(optimalSequence)
            ]
        else:
            solution = [
                [
                    self.get_C_with_preparation(index, machineIndex, optimalSequence)
                    for machineIndex in range(len(self.jobsMatrix))
                ]
                for index, _ in enumerate(optimalSequence)
            ]

        return [solution[optimalSequence.index(i)] for i in range(len(optimalSequence))]
