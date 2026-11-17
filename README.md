Hospital Emergency Queue Management System

Overview

The Hospital Emergency Queue Management System is a Python-based terminal application developed as a Data Structures and Algorithms (DSA) project.

The system manages patients in a hospital emergency department using a Min Heap (Priority Queue). Patients are treated according to their emergency priority rather than simply their arrival time. If two patients have the same priority, the patient who registered earlier is served first.

Features

- Patient Registration: Register new patients with their ID, name, age, medical condition and priority.
- Priority-Based Queue: Organise patients according to emergency levels using a Min Heap.
- Display Waiting Queue: View all waiting patients in priority order.
- Treat Next Patient: Automatically select and remove the highest-priority patient from the queue.
- Patient Search: Search for patients using their ID.
- Patient History: View records of treated patients.
- Edit Patient Priority: Update the priority of a patient who is still waiting.
- Hospital Statistics: View basic statistics about registered, waiting and treated patients.
- Data Persistence: Automatically save and load patient records using a JSON file.

Priority Levels

Priority| Emergency Level
1| Critical
2| High
3| Moderate
4| Low

Note: A smaller priority number represents a higher emergency priority. Patients with equal priority are served in their order of arrival (FIFO).

Technologies Used

- Python 3.14.7
- Data Structures and Algorithms
- Min Heap / Priority Queue
- JSON for local data storage

Data Structures and Algorithms

1. Min Heap

The main data structure used in this project is a Min Heap. It ensures that the patient with the highest emergency priority remains at the root of the heap.

2. Priority Queue

Patients are processed based on their priority. The comparison is performed using:

"(priority, arrival)"

This ensures that emergency priority is considered first and arrival order is used to break ties.

3. Searching

The system supports searching for patients using their unique patient ID.

4. Sorting

The waiting queue is displayed in sorted priority order without changing the underlying heap.

Time Complexity

Operation| Time Complexity
Insert Patient| O(log n)
Treat Next Patient| O(log n)
View Highest Priority Patient| O(1)
Search Patient by ID| O(n)
Display Sorted Queue| O(n log n)

Here, n represents the number of patients in the waiting queue.

Project Structure

Hospital-Emergency-Queue/
│
├── main.py
├── patients.json
└── README.md

- "main.py" – Contains the main application, Min Heap implementation and all patient management functions.
- "patients.json" – Stores patient records locally and preserves data between program executions.
- "README.md" – Project documentation.


Future Improvements

- Waiting time tracking.
- Department-wise patient allocation.
- Patient cancellation.
- Daily hospital activity reports.
- Graphical user interface.
- Database integration.


Contributors

- Member 1: Satvik Rastogi
- Member 2: Shababe Anwer
