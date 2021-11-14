# Production time optimization using the CDS algorithm [![Twitter][1.2]][1] [![LinkedIn][2.2]][2]

for this tutorial you need to have python 3.x installed on your machine.

"This algorithm is not optimized for professional/production use, it have been coded for students that have hard time implementing the CDS algorithm alongside the Johnson algorithm using the python programming language".

lets draw the Gantt's chart for the CDN solution in one line.

```py
"""file: test.py"""

from classes.CDS import CDS
from classes.GanttDiagram import GanttDiagram

example = [
    [5, 2, 3, 6, 7],  # machine 1
    [2, 4, 4, 5, 3],  # machine 2
    [3, 2, 5, 4, 2],  # machine 3
]

GanttDiagram(CDS(example)).showChart()
```

![GanttDiagram](https://github.com/karimGeh/CDSAlgorithm/blob/master/public/chart1.png?raw=true)

## Introduction :

In this algorithm you will find 2 classes in the **./classes** folder.
first class is the CDN class which takes in argument a 2d list each list represent the time that each job will take in the given machine.

**example:**
In the following example we have 5 jobs, each one have different timing on each machine.

```py
exampleList = [
    [5, 2, 3, 6, 7],  # machine 1
    [2, 4, 4, 5, 3],  # machine 2
    [3, 2, 5, 4, 2],  # machine 3
]
```

Lets use our CDS class on the `exampleList` and get some outputs.

First of all we should create a CDS object

```py
CDS_Object = CDS(exampleList)
```

On the `CDS_object` variable we will have access to 6 methods:

- `getSigmaJohnson(MachineOne: list[int], MachineTwo: list[int])`
- `generateTwoVirtualMachines(self, k: int) -> list[list[int]]`
- `get_C(self, jobIndex: int, machineIndex: int, sequence: list[int])`
- `get_C_max(self, sequence: list[int]) -> int`
- `get_CDS_solution(self) -> dict`
- `getSolutionAsMatrix(self, optimalSequence: list[int] | None = None)`

# `getSigmaJohnson` (static)

The first methode is **static**, `getSigmaJohnson` is simply an implementation of the Johnson rule to find the optimal sequence of jobs to reduce makespan sequence... [more in wikipedia](https://en.wikipedia.org/wiki/Johnson%27s_rule)

# `generateTwoVirtualMachines`

The second methode is `generateTwoVirtualMachines`, this method do nothing but generating a two seperate virtual machines summing the values of the first and last k machines in the `exampleList` array.

# `get_C`

The third methode is `get_C`, it takes 3 arguments a **jobIndex**, a **machineIndex** and a **sequence**, then it returns the value when the given **job** will finish its process in the given **machine** with the given **sequence**.

# `get_C_max`

The fourth methode is `get_C_max`, it takes only one arguments which is the **sequence** as list of jobs, and it returns when the whole sequence will finish processing in all machines.

# `get_CDS_solution`

The fifth methode is `get_CDS_solution`, it takes no arguments and it returns the best **sequence** that the cds algorithm could come up with. and it returns a dictionary with the optimal k, optimal time (C_max) and the optimal sequence.

```py
{
    "k": optimalK,
    "time": optimalTime,
    "sequence": optimalSequence
}
```

# GanttDiagram

To plot the Gantt's chart here comes the second class which is `GanttDiagram` in order to use this class you will need to install the _**matplotlib**_ library.

if you don't have it already installed run the following command:

```sh
pip install matplotlib
```

The `GanttDiagram` takes two arguments, the first one is the `CDS_object`, and the second one is the `sequence`. if you don't provide the sequence the algorithm will use the CDS solution sequence as default sequence. and you only need to call the `showChart()` method on the GanttDiagram object to show the chart.

```
GanttDiagram(example_CDS).showChart()
```

![GanttDiagram](https://github.com/karimGeh/CDSAlgorithm/blob/master/public/chart1.png?raw=true)

## License

MIT
**Free Software, Hell Yeah!**

[1.2]: https://img.shields.io/badge/Twitter-@karimGeh?style=flat&logo=Twitter&logoColor=white&color=1D9BF0
[2.2]: https://img.shields.io/badge/LinkedIn-Karim%20G?style=flat&logo=LinkedIn&logoColor=white&color=0A66C2
[3.2]: https://img.shields.io/badge/UpWork-Karim%20G?style=flat&logo=Upwork&logoColor=white&color=14A800

[1]: https://twitter.com/karimGeh
[2]: https://www.linkedin.com/in/karim-gehad/
[3]: https://www.upwork.com/freelancers/~0139e8dbc9c723a93a
