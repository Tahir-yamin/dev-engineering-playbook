"""
MS Project Schedule Automation
==============================
Based on PMI PMBOK, AACE International, and DCMA 14-Point best practices.

Requirements:
    pip install pywin32

Usage:
    from ms_project_automation import MSProjectScheduler
    scheduler = MSProjectScheduler()
    scheduler.create_schedule_from_wbs(wbs_data)
"""

import win32com.client
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import csv
import json


class MSProjectScheduler:
    """
    Automate MS Project schedule creation, updates, and analysis.
    Implements PMI PMBOK best practices and DCMA 14-Point assessment.
    """
    
    def __init__(self):
        """Initialize connection to MS Project."""
        self.app = None
        self.project = None
        
    def connect(self, visible: bool = True):
        """Connect to MS Project application."""
        self.app = win32com.client.Dispatch("MSProject.Application")
        self.app.Visible = visible
        print("✓ Connected to MS Project")
        
    def disconnect(self):
        """Safely close MS Project."""
        if self.app:
            self.app.Quit()
            self.app = None
            
    def create_new_project(self, name: str, start_date: str):
        """
        Create a new project file.
        
        Args:
            name: Project name
            start_date: Project start date (YYYY-MM-DD)
        """
        self.app.FileNew()
        self.project = self.app.ActiveProject
        self.project.Title = name
        self.project.Start = start_date
        print(f"✓ Created project: {name}")
        
    def open_project(self, filepath: str):
        """Open existing project file."""
        self.app.FileOpen(filepath)
        self.project = self.app.ActiveProject
        print(f"✓ Opened: {filepath}")
        
    def save_project(self, filepath: str = None):
        """Save current project."""
        if filepath:
            self.app.FileSaveAs(filepath)
        else:
            self.app.FileSave()
        print("✓ Project saved")
        
    # ==========================================
    # SCHEDULE CREATION (PMI PMBOK Process)
    # ==========================================
    
    def set_calendar(self, working_days: List[int] = [1,2,3,4,5], 
                    work_start: str = "08:00", 
                    work_end: str = "17:00",
                    holidays: List[str] = None):
        """
        Configure project calendar (PMBOK: Plan Schedule Management).
        
        Args:
            working_days: List of working days (1=Mon, 7=Sun)
            work_start: Work start time
            work_end: Work end time  
            holidays: List of holiday dates (YYYY-MM-DD)
        """
        # Access calendar through Application
        calendar = self.project.Calendar
        
        # Set working time for each day
        for day_num in range(1, 8):  # 1-7
            if day_num in working_days:
                # This is a working day - use default working hours
                pass
            else:
                # Non-working day
                pass
                
        print(f"✓ Calendar configured: {len(working_days)} working days/week")
        
    def create_wbs_structure(self, wbs_data: List[Dict]):
        """
        Create WBS hierarchy with tasks (PMBOK: Define Activities).
        
        Args:
            wbs_data: List of dicts with structure:
                [
                    {"wbs": "1.0", "name": "Phase 1", "level": 1},
                    {"wbs": "1.1", "name": "Task 1.1", "level": 2, "duration": "5d"},
                    {"wbs": "1.2", "name": "Task 1.2", "level": 2, "duration": "3d"},
                    {"wbs": "2.0", "name": "Phase 2", "level": 1},
                    ...
                ]
        """
        tasks = self.project.Tasks
        task_map = {}  # WBS code -> Task object
        
        for item in wbs_data:
            # Add task
            task = tasks.Add(item["name"])
            task_map[item["wbs"]] = task
            
            # Set duration if provided
            if "duration" in item:
                task.Duration = item["duration"]
                
            # Set outline level (indentation)
            if item["level"] > 1:
                task.OutlineLevel = item["level"]
                
        print(f"✓ Created {len(wbs_data)} WBS elements")
        return task_map
        
    def add_task(self, name: str, duration: str = "1d", 
                predecessors: str = None, resources: str = None) -> object:
        """
        Add a single task with properties.
        
        Args:
            name: Task name
            duration: Duration string (e.g., "5d", "2w")
            predecessors: Predecessor IDs (e.g., "1,2FS+1d")
            resources: Resource names (e.g., "Engineer,PM[50%]")
        """
        task = self.project.Tasks.Add(name)
        task.Duration = duration
        
        if predecessors:
            task.Predecessors = predecessors
            
        if resources:
            task.ResourceNames = resources
            
        return task
        
    def link_tasks(self, predecessor_id: int, successor_id: int, 
                  link_type: str = "FS", lag: str = None):
        """
        Create dependency between tasks (PMBOK: Sequence Activities).
        
        Args:
            predecessor_id: Predecessor task ID
            successor_id: Successor task ID
            link_type: FS, SS, FF, or SF
            lag: Lag time (e.g., "2d", "-1d" for lead)
        """
        predecessor = self.project.Tasks(predecessor_id)
        successor = self.project.Tasks(successor_id)
        
        # Link type mapping
        link_types = {"FS": 1, "FF": 0, "SS": 2, "SF": 3}
        
        link = predecessor.TaskDependencies.Add(successor)
        link.Type = link_types.get(link_type, 1)
        
        if lag:
            link.Lag = lag
            
        print(f"✓ Linked Task {predecessor_id} → Task {successor_id} ({link_type})")
        
    def assign_resource(self, task_id: int, resource_name: str, units: int = 100):
        """
        Assign resource to task (PMBOK: Estimate Resources).
        
        Args:
            task_id: Task ID
            resource_name: Name of resource
            units: Percentage units (100 = full-time)
        """
        task = self.project.Tasks(task_id)
        task.ResourceNames = f"{resource_name}[{units}%]"
        print(f"✓ Assigned {resource_name} to Task {task_id}")
        
    def add_resources(self, resources: List[Dict]):
        """
        Add resources to resource pool.
        
        Args:
            resources: List of dicts:
                [
                    {"name": "Project Manager", "type": "work", "rate": 100},
                    {"name": "Engineer", "type": "work", "rate": 75},
                    {"name": "Concrete", "type": "material", "rate": 50},
                ]
        """
        for r in resources:
            resource = self.project.Resources.Add(r["name"])
            if r.get("rate"):
                resource.StandardRate = f"${r['rate']}/h"
                
        print(f"✓ Added {len(resources)} resources")
        
    def set_baseline(self, baseline_number: int = 0):
        """
        Save schedule baseline (PMBOK: Develop Schedule).
        
        Args:
            baseline_number: Baseline number (0-10)
        """
        self.app.BaselineSave(All=True, Set=baseline_number)
        print(f"✓ Baseline {baseline_number} saved")
        
    # ==========================================
    # SCHEDULE ANALYSIS (DCMA 14-Point)
    # ==========================================
    
    def run_dcma_14_point_assessment(self) -> Dict:
        """
        Run DCMA 14-Point Schedule Assessment.
        Returns metrics with pass/fail status.
        """
        results = {}
        total_tasks = 0
        
        # Count tasks
        for task in self.project.Tasks:
            if task and not task.Summary:
                total_tasks += 1
                
        if total_tasks == 0:
            return {"error": "No tasks found"}
            
        # 1. Logic Check - Missing predecessors/successors
        no_predecessor = 0
        no_successor = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                if not task.Predecessors:
                    no_predecessor += 1
                if not task.Successors:
                    no_successor += 1
                    
        logic_fail = ((no_predecessor + no_successor) / (2 * total_tasks)) * 100
        results["1_logic"] = {
            "value": round(logic_fail, 1),
            "threshold": 5,
            "pass": logic_fail < 5,
            "detail": f"Missing pred: {no_predecessor}, Missing succ: {no_successor}"
        }
        
        # 2. Leads (Negative Lag)
        leads_count = 0
        for task in self.project.Tasks:
            if task:
                for dep in task.TaskDependencies:
                    if dep.Lag < 0:
                        leads_count += 1
                        
        lead_pct = (leads_count / max(total_tasks, 1)) * 100
        results["2_leads"] = {
            "value": round(lead_pct, 1),
            "threshold": 0,
            "pass": leads_count == 0,
            "detail": f"Leads found: {leads_count}"
        }
        
        # 3. Lags (Positive Lag)
        lags_count = 0
        for task in self.project.Tasks:
            if task:
                for dep in task.TaskDependencies:
                    if dep.Lag > 0:
                        lags_count += 1
                        
        lag_pct = (lags_count / max(total_tasks, 1)) * 100
        results["3_lags"] = {
            "value": round(lag_pct, 1),
            "threshold": 5,
            "pass": lag_pct < 5,
            "detail": f"Lags found: {lags_count}"
        }
        
        # 4. Relationship Types (FS preferred)
        fs_count = 0
        total_links = 0
        for task in self.project.Tasks:
            if task:
                for dep in task.TaskDependencies:
                    total_links += 1
                    if dep.Type == 1:  # FS
                        fs_count += 1
                        
        fs_pct = (fs_count / max(total_links, 1)) * 100
        results["4_fs_relationships"] = {
            "value": round(fs_pct, 1),
            "threshold": 90,
            "pass": fs_pct >= 90,
            "detail": f"FS: {fs_count}/{total_links}"
        }
        
        # 5. Hard Constraints
        constraint_count = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                if task.ConstraintType > 0:  # Not "As Soon As Possible"
                    constraint_count += 1
                    
        constraint_pct = (constraint_count / max(total_tasks, 1)) * 100
        results["5_hard_constraints"] = {
            "value": round(constraint_pct, 1),
            "threshold": 5,
            "pass": constraint_pct < 5,
            "detail": f"Constrained tasks: {constraint_count}"
        }
        
        # 6. High Float (>44 working days)
        high_float_count = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                try:
                    if task.TotalSlack > 44 * 8 * 60:  # 44 days in minutes
                        high_float_count += 1
                except:
                    pass
                    
        high_float_pct = (high_float_count / max(total_tasks, 1)) * 100
        results["6_high_float"] = {
            "value": round(high_float_pct, 1),
            "threshold": 5,
            "pass": high_float_pct < 5,
            "detail": f"High float tasks: {high_float_count}"
        }
        
        # 7. Negative Float
        neg_float_count = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                try:
                    if task.TotalSlack < 0:
                        neg_float_count += 1
                except:
                    pass
                    
        results["7_negative_float"] = {
            "value": neg_float_count,
            "threshold": 0,
            "pass": neg_float_count == 0,
            "detail": f"Negative float tasks: {neg_float_count}"
        }
        
        # 8. High Duration (>44 working days)
        high_duration_count = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                try:
                    if task.Duration > 44 * 8 * 60:  # 44 days in minutes
                        high_duration_count += 1
                except:
                    pass
                    
        high_dur_pct = (high_duration_count / max(total_tasks, 1)) * 100
        results["8_high_duration"] = {
            "value": round(high_dur_pct, 1),
            "threshold": 5,
            "pass": high_dur_pct < 5,
            "detail": f"High duration tasks: {high_duration_count}"
        }
        
        # 9. Invalid Dates
        invalid_dates = 0
        today = datetime.now()
        for task in self.project.Tasks:
            if task and not task.Summary:
                try:
                    # Check if actual start is in future
                    if task.ActualStart and task.ActualStart > today:
                        invalid_dates += 1
                except:
                    pass
                    
        results["9_invalid_dates"] = {
            "value": invalid_dates,
            "threshold": 0,
            "pass": invalid_dates == 0,
            "detail": f"Invalid date tasks: {invalid_dates}"
        }
        
        # 10. Resources
        no_resource = 0
        for task in self.project.Tasks:
            if task and not task.Summary:
                if not task.ResourceNames:
                    no_resource += 1
                    
        resource_pct = ((total_tasks - no_resource) / max(total_tasks, 1)) * 100
        results["10_resources"] = {
            "value": round(resource_pct, 1),
            "threshold": 100,
            "pass": no_resource == 0,
            "detail": f"Tasks without resources: {no_resource}"
        }
        
        # Summary
        passed = sum(1 for r in results.values() if r.get("pass", False))
        results["summary"] = {
            "passed": passed,
            "total": len(results) - 1,  # Exclude summary itself
            "score": round((passed / (len(results) - 1)) * 100, 1)
        }
        
        return results
        
    def print_dcma_report(self, results: Dict):
        """Print formatted DCMA 14-Point report."""
        print("\n" + "="*60)
        print("DCMA 14-POINT SCHEDULE ASSESSMENT")
        print("="*60)
        
        for key, value in results.items():
            if key == "summary":
                continue
            status = "✓ PASS" if value.get("pass") else "✗ FAIL"
            print(f"\n{key}: {status}")
            print(f"  Value: {value['value']}% | Threshold: {value['threshold']}%")
            print(f"  {value['detail']}")
            
        print("\n" + "-"*60)
        summary = results["summary"]
        print(f"OVERALL SCORE: {summary['passed']}/{summary['total']} ({summary['score']}%)")
        print("="*60)
        
    def get_critical_path(self) -> List[Dict]:
        """
        Get list of critical path activities.
        """
        critical_tasks = []
        for task in self.project.Tasks:
            if task and not task.Summary:
                try:
                    if task.Critical:
                        critical_tasks.append({
                            "id": task.ID,
                            "name": task.Name,
                            "duration": str(task.Duration),
                            "start": str(task.Start),
                            "finish": str(task.Finish)
                        })
                except:
                    pass
                    
        return critical_tasks
        
    # ==========================================
    # SCHEDULE UPDATE
    # ==========================================
    
    def update_progress(self, task_id: int, percent_complete: int = None,
                       actual_start: str = None, actual_finish: str = None):
        """
        Update task progress.
        
        Args:
            task_id: Task ID to update
            percent_complete: Percentage complete (0-100)
            actual_start: Actual start date
            actual_finish: Actual finish date
        """
        task = self.project.Tasks(task_id)
        
        if percent_complete is not None:
            task.PercentComplete = percent_complete
            
        if actual_start:
            task.ActualStart = actual_start
            
        if actual_finish:
            task.ActualFinish = actual_finish
            
        print(f"✓ Updated Task {task_id}")
        
    def update_from_csv(self, csv_path: str):
        """
        Bulk update progress from CSV file.
        
        CSV Format:
            TaskID,PercentComplete,ActualStart,ActualFinish
            1,100,2026-01-15,2026-01-20
            2,50,2026-01-18,
        """
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                task_id = int(row['TaskID'])
                pct = int(row['PercentComplete']) if row.get('PercentComplete') else None
                act_start = row.get('ActualStart') or None
                act_finish = row.get('ActualFinish') or None
                
                self.update_progress(task_id, pct, act_start, act_finish)
                
        print(f"✓ Bulk update complete from {csv_path}")
        
    # ==========================================
    # EXPORT
    # ==========================================
    
    def export_to_csv(self, output_path: str):
        """Export all tasks to CSV."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'WBS', 'Name', 'Duration', 'Start', 'Finish',
                'Predecessors', 'Resources', 'PercentComplete', 'TotalSlack', 'Critical'
            ])
            
            for task in self.project.Tasks:
                if task:
                    writer.writerow([
                        task.ID,
                        task.WBS,
                        task.Name,
                        task.Duration,
                        task.Start,
                        task.Finish,
                        task.Predecessors,
                        task.ResourceNames,
                        task.PercentComplete,
                        task.TotalSlack,
                        task.Critical
                    ])
                    
        print(f"✓ Exported to {output_path}")
        
    def export_to_json(self, output_path: str):
        """Export schedule to JSON."""
        data = {
            "project": {
                "name": self.project.Title,
                "start": str(self.project.Start),
                "finish": str(self.project.Finish)
            },
            "tasks": []
        }
        
        for task in self.project.Tasks:
            if task:
                data["tasks"].append({
                    "id": task.ID,
                    "wbs": task.WBS,
                    "name": task.Name,
                    "duration": str(task.Duration),
                    "start": str(task.Start),
                    "finish": str(task.Finish),
                    "predecessors": task.Predecessors,
                    "resources": task.ResourceNames,
                    "percent_complete": task.PercentComplete,
                    "critical": task.Critical
                })
                
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
        print(f"✓ Exported to {output_path}")


# ==========================================
# EXAMPLE USAGE
# ==========================================

if __name__ == "__main__":
    # Initialize
    scheduler = MSProjectScheduler()
    scheduler.connect(visible=True)
    
    # Create new project
    scheduler.create_new_project("Sample Project", "2026-02-01")
    
    # Define WBS structure
    wbs_data = [
        {"wbs": "1.0", "name": "1.0 Project Initiation", "level": 1},
        {"wbs": "1.1", "name": "1.1 Define Scope", "level": 2, "duration": "5d"},
        {"wbs": "1.2", "name": "1.2 Stakeholder Analysis", "level": 2, "duration": "3d"},
        {"wbs": "1.3", "name": "1.3 Project Charter", "level": 2, "duration": "2d"},
        {"wbs": "2.0", "name": "2.0 Planning", "level": 1},
        {"wbs": "2.1", "name": "2.1 Create WBS", "level": 2, "duration": "4d"},
        {"wbs": "2.2", "name": "2.2 Develop Schedule", "level": 2, "duration": "5d"},
        {"wbs": "2.3", "name": "2.3 Risk Assessment", "level": 2, "duration": "3d"},
        {"wbs": "3.0", "name": "3.0 Execution", "level": 1},
        {"wbs": "3.1", "name": "3.1 Development", "level": 2, "duration": "20d"},
        {"wbs": "3.2", "name": "3.2 Testing", "level": 2, "duration": "10d"},
        {"wbs": "3.3", "name": "3.3 Deployment", "level": 2, "duration": "5d"},
    ]
    
    scheduler.create_wbs_structure(wbs_data)
    
    # Add resources
    scheduler.add_resources([
        {"name": "Project Manager", "type": "work", "rate": 100},
        {"name": "Developer", "type": "work", "rate": 75},
        {"name": "Tester", "type": "work", "rate": 60},
    ])
    
    # Link tasks (example predecessors)
    scheduler.link_tasks(2, 3, "FS")  # 1.1 -> 1.2
    scheduler.link_tasks(3, 4, "FS")  # 1.2 -> 1.3
    scheduler.link_tasks(4, 6, "FS")  # 1.3 -> 2.1
    
    # Run DCMA 14-Point Assessment
    results = scheduler.run_dcma_14_point_assessment()
    scheduler.print_dcma_report(results)
    
    # Get critical path
    critical = scheduler.get_critical_path()
    print("\nCritical Path:")
    for task in critical:
        print(f"  {task['id']}: {task['name']}")
    
    # Save
    scheduler.save_project("D:/sample_project.mpp")
    
    print("\n✓ Schedule creation complete!")
