Note: this a fork of the [original Gitlab repository](https://gitlab.com/qosf/qml-mooc) of the MOOC, along with the official solutions. Since Peter Wittek, the creator of the MOOC, [disappeared in an avalanche](https://www.cbc.ca/news/canada/toronto/peter-wittek-trisul-rescue-1.5305924) in October 2019, the future of the MOOC on [edX](https://www.edx.org/course/quantum-machine-learning) is uncertain. This repository, along with the [videos](https://www.youtube.com/watch?v=QtWCmO_KIlg&list=PLmRxgFnCIhaMgvot-Xuym_hn69lmzIokg), should allow his work to survive and benefit everyone who wants to learn about quantum machine learning! Enjoy!

# Quantum Machine Learning

The pace of development in quantum computing mirrors the rapid advances made in machine learning and artificial intelligence. It is natural to ask whether quantum technologies could boost learning algorithms: this field of enquiry is called quantum machine learning. This massively open online online course (MOOC) on [edX](https://www.edx.org/course/quantum-machine-learning) is offered by the University of Toronto on edX with an emphasis on what benefits current and near-future quantum technologies may bring to machine learning. These notebooks contain the lecture notes and the code for the course. The content is organized in four modules, with an additional introductory module to the course itself.

Since the course is hands-on, we found it important that you can try the code on actual quantum computers if you want to. There isn't a single, unified programming framework that would allow to address all available quantum hardware. For this reason, the notebooks are available in two versions: one in Qiskit targeting the IBM Q hardware and the Forest SDK targetting the Rigetti quantum computer. The notebooks also cover quantum annealing -- for that, the D-Wave Ocean Suite is used. For more details on setting up your computational environment locally, refer to the notebooks in Module 0.

The code snippets in the notebooks are licensed under the MIT License. The text and figures are licensed under the Creative Commons Attribution 4.0 International Public License (CC-BY-4.0).

# Prerequisites

Python and a good command of linear algebra are necessary. Experience with machine learning helps.

# Structure

**Module 0: Introduction**

00_Course_Introduction.ipynb

00_Introduction_to_Cirq.ipynb

00_Introduction_to_Qiskit.ipynb

00_Introduction_to_the_Forest_SDK.ipynb

**Module 1: Quantum Systems**

01_Classical_and_Quantum_Probability_Distributions.ipynb

02_Measurements_and_Mixed_States.ipynb

03_Evolution_in_Closed_and_Open_Systems.ipynb

04_Classical_and_Quantum_Many-Body_Physics.ipynb

**Module 2: Quantum Computation**

05_Gate-Model_Quantum_Computing.ipynb

06_Adiabatic_Quantum_Computing.ipynb

07_Variational_Circuits.ipynb

08_Sampling_a_Thermal_State.ipynb

**Module 3: Classical-quantum hybrid learning algorithms**

09_Discrete_Optimization_and_Ensemble_Learning.ipynb

10_Discrete_Optimization_and_Unsupervised_Learning.ipynb

11_Kernel_Methods.ipynb

12_Training_Probabilistic_Graphical_Models.ipynb

**Module 4: Coherent Learning Protocols**

13_Quantum_Phase_Estimation.ipynb

14_Quantum_Matrix_Inversion.ipynb

# Assignments

The assignments are included, but without the solutions. The master version is developed in a separate private repository. If you are an interested in using them for your own lectures, please contact us to give you access.

# Contributing

We welcome contributions - simply fork the repository, and then make a pull request containing your contribution. We would especially love to see the course extended to other open source quantum computing frameworks. We also encourage bug reports and suggestions for enhancements.
