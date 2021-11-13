"""
  Created by :  Karim Gehad
  On         :  13/11/2021

  email      :  karimgehad@outlook.com
  github     :  https://github.com/karimGeh
  linkedIn   :  https://www.linkedin.com/in/karim-gehad
"""

class CDS:
    def __init__(self, jobsMatrix: list[list[int]]) -> None:
        self.jobsMatrix = jobsMatrix

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
            return self.get_C(jobIndex - 1, 0, sequence) + self.jobsMatrix[0][sequence[jobIndex]]

        return (
            max(
                self.get_C(jobIndex - 1, machineIndex, sequence),
                self.get_C(jobIndex, machineIndex - 1, sequence),
            )
            + self.jobsMatrix[machineIndex][sequence[jobIndex]]
        )

    def get_C_max(self, sequence: list[int]) -> int:
        # getting C max is nothing but getting
        # when the last job will finish
        return self.get_C(
            len(self.jobsMatrix[0]) - 1,  # last job index
            len(self.jobsMatrix) - 1,  # last machine index
            sequence,
        )

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

    def getSolutionAsMatrix(self, optimalSequence: list[int] = None):
        if not optimalSequence:
            optimalSequence = self.get_CDS_solution()["sequence"]

        # return [
        #     [
        #         self.get_C(jobIndex, machineIndex, optimalSequence) for jobIndex in range(len(optimalSequence))
        #     ] for machineIndex in range(len(self.jobsMatrix))
        # ]

        solution = [
            [self.get_C(jobIndex, machineIndex, optimalSequence) for machineIndex in range(len(self.jobsMatrix))]
            for jobIndex in range(len(optimalSequence))
        ]

        return [solution[optimalSequence.index(i)] for i in range(len(optimalSequence))]
