# Microsoft Project Import Guide

## Column Mapping (Excel -> MS Project)

When importing the generated Excel file (`Project_Schedule_MSP_Export_v10.xlsx`) into Microsoft Project, use the "New Map" feature and define the following mappings:

| From: Excel Field | To: Microsoft Project Field | Data Type |
| :--- | :--- | :--- |
| **Task Name** | **Name** | Text |
| **Duration** | **Duration** | Text |
| **Predecessors** | **Predecessors** | Text |
| **Outline Level** | **Outline Level** | Text |
| **MSP_ID** | **ID** | Text |

## Import Settings
1.  **Format**: Excel Workbook
2.  **Map**: Create New Map
3.  **Mode**: Append to the end of the active project (or As a new project)
4.  **Tasks Mapping**: Ensure the checkbox "Tasks" is selected.
5.  **Headers**: "My data has headers" should be **CHECKED**.

> **Note**: Mapping `MSP_ID` to `ID` is crucial for maintaining the correct sort order and linkage, especially when predecessors reference specific Row IDs.
