# Introduction

I am happy :smile to introduce you to

**Title**: *Exam Timetable Scheduler: A Conflict-Free Course Scheduling Solution Utilizing the Time-Matrix Algorithm*

In the realm of academic institutions, efficient scheduling of exams is a critical aspect that contributes to the smooth functioning of educational systems. The process of organizing a comprehensive and conflict-free exam timetable can be a complex undertaking, particularly when faced with a myriad of courses, faculty constraints, and student preferences. To address this challenge, the development of an intelligent and automated Exam Timetable Scheduler has emerged as a vital tool for educational institutions.

This project introduces an innovative approach to exam scheduling by leveraging the power of the Time-Matrix Algorithm. The primary objective of this scheduler is to generate optimized exam timetables that eliminate any conflicts among the courses, ensuring fairness, convenience, and efficiency for both students and faculty members. By employing an algorithmic framework that efficiently analyzes and organizes the available resources, this solution aims to streamline the entire scheduling process, reducing manual effort and minimizing human errors.

The Time-Matrix Algorithm, the backbone of our scheduler, is a sophisticated mathematical model that strategically assigns courses to specific time slots based on a comprehensive set of constraints and preferences. This algorithm takes into account various factors such as course durations, student enrollment, faculty availability, and room capacities, while meticulously designing a timetable that meets the unique requirements of the academic institution.

By utilizing this algorithmic approach, the exam timetable scheduler can achieve conflict-free scheduling, eliminating any overlaps or clashes between courses. This ensures that students are not burdened with the predicament of having to choose between conflicting exams, enabling them to focus on their studies and perform optimally. Additionally, faculty members benefit from an organized schedule, enabling them to allocate their time effectively and provide adequate attention to each examination.

Furthermore, this project aims to provide a user-friendly interface that allows administrators, faculty members, and students to easily input their preferences, constraints, and relevant data. The scheduler processes this information, leveraging the Time-Matrix Algorithm, and generates an optimized exam timetable that adheres to the specified parameters. Through the seamless integration of technology and education, this solution offers a systematic and efficient approach to exam scheduling, contributing to the overall enhancement of academic operations.

In conclusion, the Exam Timetable Scheduler presented in this project offers an innovative and effective solution to the intricate task of course scheduling. By harnessing the power of the Time-Matrix Algorithm, the scheduler ensures a conflict-free timetable that caters to the needs of students and faculty members alike. As educational institutions strive for efficiency and fairness in their operations, this project seeks to provide a valuable tool that optimizes the exam scheduling process, ultimately enhancing the learning experience for all stakeholders involved.



# How The Algorithm Works
## Overview
When it's time for scheduling the timetable for any department, the algorithm takes in all the courses offered in the department for a semester and schedule them accordingly.

By default, all the cells in the *Time-matrix* table have 0 as their value
- 0 means available for scheduling
- 1 means it contains a course already
- -1 means unavailable for scheduling

Each *column* in the table contains *a course*, *a time slot* and *a venue*.
The *rows* contain the *available days*.


## The WorkFlow
### Shuffling The List of Courses

The courses are shuffled so that the timetable generated will be different from the previous one.

### Random Scheduling

A *cell* is chosen randomly from the list of available cells in a column


### Conflict Check

If the venue of the column is not available at the time slot of the day of the cell chosen, another cell is chosen randomly until the condition for scheduling is met, or the column runs out of cells.

### Changing The Time Slot

IF the column runs out of cells, another time slot is chosen randomly and assign to the column for another round of scheduling.

This process is repeated until the algorithm runs out of time slots to choose from.

### Changing The Venue

If the course has not yet been scheduled, the algorithm changes the venue of the column to another one with higher capacity until the algorithm runs out of venues to choose from.

### Reiteration

This process is repeated for all the column in the *time-matrix* table.

# Portable softcopy

The timetable can be downloaded in form of pdf

# Prototype

- [TimeTable](http://ecclesiastes.pythonanywhere.com)
- [KDLT TimeTable](http://ecclesiastes.pythonanywhere.com/venue/KDLT)
- [CLT TimeTable](http://ecclesiastes.pythonanywhere.com/venue/CLT)
- [TimeTable PDF](http://ecclesiastes.pythonanywhere.com/pdf)
- [Time-Matrix Table](http://ecclesiastes.pythonanywhere.com/matrix)
# Thanks!

