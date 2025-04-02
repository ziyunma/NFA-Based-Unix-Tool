# Efficient NFA-Based Regex Matching and Unix Tool Reimplementation
-Theory of Computing Project Spring24-

This project implements a nondeterministic finite automaton (NFA) matcher in Python, exploring efficient simulation of nondeterminism on deterministic hardware. Unlike naive backtracking (O(2ⁿ) time) or full NFA-to-DFA conversion (O(2^|Q|) space), this approach runs in O(|δ|n) time, making it significantly more efficient. The project includes:

* Regular Expression Parsing – Converting regex patterns into NFA representations.

* Efficient NFA Execution – Running input strings through the NFA using a linear-time algorithm.

* Unix Tool Reimplementation – Implementing key features of grep and sed, including backreferences and conditional branching.

* Turing-Completeness & Complexity Exploration – Demonstrating sed's Turing-completeness and proving grep with backreferences is NP-complete by implementing a SAT solver.
