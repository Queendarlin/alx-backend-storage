MySQL Advanced Tasks README

This repository contains SQL scripts and stored procedures created to solve various database tasks.

## Task Descriptions

1. **Safe Divide Function**: Implements a SQL function `SafeDiv` that divides two integers safely, returning 0 if the divisor is 0.
   
2. **Students Need Meeting View**: Creates a SQL view `need_meeting` that lists students with scores below 80 and either no recorded meeting or a meeting older than 1 month.
   
3. **Compute Average Weighted Score for User**: Defines a stored procedure `ComputeAverageWeightedScoreForUser` to compute and store the average weighted score for a given student.
   
4. **Compute Average Weighted Score for All Users**: Defines a stored procedure `ComputeAverageWeightedScoreForUsers` to compute and store the average weighted score for all students.

## Setup

### Prerequisites

- MySQL server installed and running
- Access to create databases, tables, functions, and procedures
