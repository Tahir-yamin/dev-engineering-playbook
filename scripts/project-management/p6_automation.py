"""
Primavera P6 Schedule Automation
================================
Based on PMI PMBOK, AACE International, and DCMA 14-Point best practices.
Works with XER files (export from P6 Desktop).

Requirements:
    pip install xerparser pandas

Usage:
    from p6_automation import P6ScheduleAnalyzer
    analyzer = P6ScheduleAnalyzer("project.xer")
    results = analyzer.run_dcma_14_point_assessment()
"""

from xerparser import Xer
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import csv
import json
import os

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class P6ScheduleAnalyzer:
    """
    Analyze Primavera P6 XER files using DCMA 14-Point assessment.
    """
    
    def __init__(self, xer_path: str = None):
        """
        Initialize P6 analyzer.
        
        Args:
            xer_path: Path to XER file
        """
        self.xer = None
        self.xer_path = xer_path
        if xer_path:
            self.load_xer(xer_path)
            
    def load_xer(self, xer_path: str):
        """Load XER file."""
        self.xer = Xer.reader(xer_path)
        self.xer_path = xer_path
        print(f"✓ Loaded XER: {xer_path}")
        
    # ==========================================
    # SCHEDULE ANALYSIS
    # ==========================================
    
    def get_project_info(self) -> Dict:
        """Get project summary information."""
        if not self.xer or not self.xer.projects:
            return {"error": "No project loaded"}
            
        project = list(self.xer.projects.values())[0]
        
        return {
            "name": project.name,
            "id": project.proj_id,
            "start_date": str(project.plan_start_date) if hasattr(project, 'plan_start_date') else "N/A",
            "finish_date": str(project.plan_end_date) if hasattr(project, 'plan_end_date') else "N/A",
            "total_activities": len(list(self.xer.activities)),
            "total_resources": len(list(self.xer.resources)) if self.xer.resources else 0
        }
        
    def get_all_activities(self) -> List[Dict]:
        """Get all activities with details."""
        activities = []
        
        for activity in self.xer.activities:
            activities.append({
                "activity_id": activity.activity_id,
                "name": activity.name,
                "duration": activity.original_duration,
                "remaining_duration": activity.remaining_duration,
                "start": str(activity.start_date) if activity.start_date else None,
                "finish": str(activity.finish_date) if activity.finish_date else None,
                "percent_complete": activity.phys_complete_pct if hasattr(activity, 'phys_complete_pct') else 0,
                "total_float": activity.total_float if hasattr(activity, 'total_float') else 0,
                "is_critical": activity.total_float == 0 if hasattr(activity, 'total_float') else False
            })
            
        return activities
        
    def get_critical_path(self) -> List[Dict]:
        """Get critical path activities (zero float)."""
        critical = []
        
        for activity in self.xer.activities:
            if hasattr(activity, 'total_float') and activity.total_float == 0:
                critical.append({
                    "activity_id": activity.activity_id,
                    "name": activity.name,
                    "duration": activity.original_duration,
                    "start": str(activity.start_date) if activity.start_date else None,
                    "finish": str(activity.finish_date) if activity.finish_date else None
                })
                
        return critical
        
    def run_dcma_14_point_assessment(self) -> Dict:
        """
        Run DCMA 14-Point Schedule Assessment on XER file.
        """
        results = {}
        
        # Get all activities (non-summary)
        activities = list(self.xer.activities)
        total = len(activities)
        
        if total == 0:
            return {"error": "No activities found"}
            
        # 1. Logic Check - Missing predecessors/successors
        no_pred = 0
        no_succ = 0
        
        for activity in activities:
            if hasattr(activity, 'predecessors'):
                if not activity.predecessors or len(list(activity.predecessors)) == 0:
                    no_pred += 1
            else:
                no_pred += 1
                
            if hasattr(activity, 'successors'):
                if not activity.successors or len(list(activity.successors)) == 0:
                    no_succ += 1
            else:
                no_succ += 1
                
        logic_pct = ((no_pred + no_succ) / (2 * total)) * 100
        results["1_logic"] = {
            "value": round(logic_pct, 1),
            "threshold": 5,
            "pass": logic_pct < 5,
            "detail": f"No predecessor: {no_pred}, No successor: {no_succ}"
        }
        
        # 2. Leads (Negative Lag)
        leads = 0
        total_rels = 0
        
        for activity in activities:
            if hasattr(activity, 'predecessors'):
                for rel in activity.predecessors:
                    total_rels += 1
                    if hasattr(rel, 'lag') and rel.lag < 0:
                        leads += 1
                        
        lead_pct = (leads / max(total, 1)) * 100
        results["2_leads"] = {
            "value": round(lead_pct, 1),
            "threshold": 0,
            "pass": leads == 0,
            "detail": f"Leads found: {leads}"
        }
        
        # 3. Lags (Positive Lag)
        lags = 0
        
        for activity in activities:
            if hasattr(activity, 'predecessors'):
                for rel in activity.predecessors:
                    if hasattr(rel, 'lag') and rel.lag > 0:
                        lags += 1
                        
        lag_pct = (lags / max(total, 1)) * 100
        results["3_lags"] = {
            "value": round(lag_pct, 1),
            "threshold": 5,
            "pass": lag_pct < 5,
            "detail": f"Lags found: {lags}"
        }
        
        # 4. Relationship Types (FS preferred)
        fs_count = 0
        other_count = 0
        
        for activity in activities:
            if hasattr(activity, 'predecessors'):
                for rel in activity.predecessors:
                    if hasattr(rel, 'link') and rel.link == 'FS':
                        fs_count += 1
                    else:
                        other_count += 1
                        
        total_links = fs_count + other_count
        fs_pct = (fs_count / max(total_links, 1)) * 100
        results["4_fs_relationships"] = {
            "value": round(fs_pct, 1),
            "threshold": 90,
            "pass": fs_pct >= 90,
            "detail": f"FS: {fs_count}/{total_links}"
        }
        
        # 5. Constraints
        constrained = 0
        
        for activity in activities:
            if hasattr(activity, 'constraint_type') and activity.constraint_type:
                constrained += 1
                
        const_pct = (constrained / max(total, 1)) * 100
        results["5_hard_constraints"] = {
            "value": round(const_pct, 1),
            "threshold": 5,
            "pass": const_pct < 5,
            "detail": f"Constrained: {constrained}"
        }
        
        # 6. High Float (>44 days)
        high_float = 0
        
        for activity in activities:
            if hasattr(activity, 'total_float') and activity.total_float:
                if activity.total_float > 44:
                    high_float += 1
                    
        hf_pct = (high_float / max(total, 1)) * 100
        results["6_high_float"] = {
            "value": round(hf_pct, 1),
            "threshold": 5,
            "pass": hf_pct < 5,
            "detail": f"High float: {high_float}"
        }
        
        # 7. Negative Float
        neg_float = 0
        
        for activity in activities:
            if hasattr(activity, 'total_float') and activity.total_float:
                if activity.total_float < 0:
                    neg_float += 1
                    
        results["7_negative_float"] = {
            "value": neg_float,
            "threshold": 0,
            "pass": neg_float == 0,
            "detail": f"Negative float: {neg_float}"
        }
        
        # 8. High Duration (>44 days)
        high_dur = 0
        
        for activity in activities:
            if hasattr(activity, 'original_duration') and activity.original_duration:
                if activity.original_duration > 44:
                    high_dur += 1
                    
        hd_pct = (high_dur / max(total, 1)) * 100
        results["8_high_duration"] = {
            "value": round(hd_pct, 1),
            "threshold": 5,
            "pass": hd_pct < 5,
            "detail": f"High duration: {high_dur}"
        }
        
        # 9. Invalid Dates
        invalid = 0
        today = datetime.now()
        
        for activity in activities:
            if hasattr(activity, 'actual_start_date') and activity.actual_start_date:
                if activity.actual_start_date > today:
                    invalid += 1
                    
        results["9_invalid_dates"] = {
            "value": invalid,
            "threshold": 0,
            "pass": invalid == 0,
            "detail": f"Invalid dates: {invalid}"
        }
        
        # 10. Resources
        no_resource = 0
        
        for activity in activities:
            if hasattr(activity, 'resources'):
                if not activity.resources or len(list(activity.resources)) == 0:
                    no_resource += 1
            else:
                no_resource += 1
                
        res_pct = ((total - no_resource) / max(total, 1)) * 100
        results["10_resources"] = {
            "value": round(res_pct, 1),
            "threshold": 100,
            "pass": no_resource == 0,
            "detail": f"Without resources: {no_resource}"
        }
        
        # Summary
        passed = sum(1 for r in results.values() if r.get("pass", False))
        results["summary"] = {
            "passed": passed,
            "total": 10,
            "score": round((passed / 10) * 100, 1),
            "activities_analyzed": total
        }
        
        return results
        
    def print_dcma_report(self, results: Dict = None):
        """Print formatted DCMA 14-Point report."""
        if results is None:
            results = self.run_dcma_14_point_assessment()
            
        print("\n" + "="*60)
        print("DCMA 14-POINT SCHEDULE ASSESSMENT - P6 XER")
        print("="*60)
        print(f"File: {self.xer_path}")
        
        for key, value in results.items():
            if key == "summary":
                continue
            status = "✓ PASS" if value.get("pass") else "✗ FAIL"
            print(f"\n{key}: {status}")
            print(f"  Value: {value['value']} | Threshold: {value['threshold']}")
            print(f"  {value['detail']}")
            
        print("\n" + "-"*60)
        summary = results["summary"]
        print(f"OVERALL SCORE: {summary['passed']}/{summary['total']} ({summary['score']}%)")
        print(f"Activities Analyzed: {summary['activities_analyzed']}")
        print("="*60)
        
    # ==========================================
    # EXPORT FUNCTIONS
    # ==========================================
    
    def export_to_csv(self, output_path: str):
        """Export activities to CSV."""
        activities = self.get_all_activities()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if activities:
                writer = csv.DictWriter(f, fieldnames=activities[0].keys())
                writer.writeheader()
                writer.writerows(activities)
                
        print(f"✓ Exported {len(activities)} activities to {output_path}")
        
    def export_to_json(self, output_path: str):
        """Export schedule to JSON."""
        data = {
            "project": self.get_project_info(),
            "activities": self.get_all_activities(),
            "critical_path": self.get_critical_path(),
            "dcma_assessment": self.run_dcma_14_point_assessment()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
        print(f"✓ Exported to {output_path}")
        
    def export_to_excel(self, output_path: str):
        """Export to Excel (requires pandas)."""
        if not HAS_PANDAS:
            print("✗ pandas required: pip install pandas openpyxl")
            return
            
        activities = self.get_all_activities()
        df = pd.DataFrame(activities)
        df.to_excel(output_path, index=False, sheet_name='Activities')
        print(f"✓ Exported to {output_path}")
        
    def to_dataframe(self):
        """Convert activities to pandas DataFrame."""
        if not HAS_PANDAS:
            print("✗ pandas required: pip install pandas")
            return None
            
        return pd.DataFrame(self.get_all_activities())
        
    # ==========================================
    # SCHEDULE COMPARISON
    # ==========================================
    
    def compare_with_baseline(self, baseline_xer_path: str) -> Dict:
        """
        Compare current schedule with baseline XER.
        
        Args:
            baseline_xer_path: Path to baseline XER file
        """
        baseline = P6ScheduleAnalyzer(baseline_xer_path)
        
        current_activities = {a['activity_id']: a for a in self.get_all_activities()}
        baseline_activities = {a['activity_id']: a for a in baseline.get_all_activities()}
        
        comparison = {
            "added": [],
            "removed": [],
            "changed_duration": [],
            "changed_dates": []
        }
        
        # Find added activities
        for act_id in current_activities:
            if act_id not in baseline_activities:
                comparison["added"].append(current_activities[act_id])
                
        # Find removed activities
        for act_id in baseline_activities:
            if act_id not in current_activities:
                comparison["removed"].append(baseline_activities[act_id])
                
        # Find changed activities
        for act_id in current_activities:
            if act_id in baseline_activities:
                curr = current_activities[act_id]
                base = baseline_activities[act_id]
                
                if curr['duration'] != base['duration']:
                    comparison["changed_duration"].append({
                        "activity_id": act_id,
                        "name": curr['name'],
                        "baseline_duration": base['duration'],
                        "current_duration": curr['duration']
                    })
                    
                if curr['start'] != base['start'] or curr['finish'] != base['finish']:
                    comparison["changed_dates"].append({
                        "activity_id": act_id,
                        "name": curr['name'],
                        "baseline_start": base['start'],
                        "current_start": curr['start'],
                        "baseline_finish": base['finish'],
                        "current_finish": curr['finish']
                    })
                    
        return comparison


class P6ScheduleCreator:
    """
    Create Primavera P6 compatible schedule data.
    Note: Direct P6 file creation requires P6 SDK or COM automation.
    This class generates data that can be imported into P6.
    """
    
    def __init__(self, project_name: str, start_date: str):
        """
        Initialize schedule creator.
        
        Args:
            project_name: Name of project
            start_date: Project start date (YYYY-MM-DD)
        """
        self.project_name = project_name
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.activities = []
        self.resources = []
        self.relationships = []
        
    def add_activity(self, activity_id: str, name: str, duration: int,
                    wbs: str = None, calendar: str = "Standard"):
        """
        Add activity to schedule.
        
        Args:
            activity_id: Unique activity ID
            name: Activity name
            duration: Duration in days
            wbs: WBS code
            calendar: Calendar name
        """
        self.activities.append({
            "activity_id": activity_id,
            "name": name,
            "duration": duration,
            "wbs": wbs or "",
            "calendar": calendar
        })
        
    def add_relationship(self, predecessor_id: str, successor_id: str,
                        rel_type: str = "FS", lag: int = 0):
        """
        Add relationship between activities.
        
        Args:
            predecessor_id: Predecessor activity ID
            successor_id: Successor activity ID
            rel_type: Relationship type (FS, SS, FF, SF)
            lag: Lag in days
        """
        self.relationships.append({
            "predecessor": predecessor_id,
            "successor": successor_id,
            "type": rel_type,
            "lag": lag
        })
        
    def add_resource(self, resource_id: str, name: str, 
                    resource_type: str = "Labor"):
        """
        Add resource to resource pool.
        """
        self.resources.append({
            "resource_id": resource_id,
            "name": name,
            "type": resource_type
        })
        
    def export_for_p6_import(self, output_dir: str):
        """
        Export schedule data for P6 import (CSV format).
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Export activities
        with open(f"{output_dir}/activities.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['activity_id', 'name', 'duration', 'wbs', 'calendar'])
            writer.writeheader()
            writer.writerows(self.activities)
            
        # Export relationships
        with open(f"{output_dir}/relationships.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['predecessor', 'successor', 'type', 'lag'])
            writer.writeheader()
            writer.writerows(self.relationships)
            
        # Export resources
        with open(f"{output_dir}/resources.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['resource_id', 'name', 'type'])
            writer.writeheader()
            writer.writerows(self.resources)
            
        print(f"✓ Exported P6 import files to {output_dir}")
        print("  Import into P6: File → Import → Spreadsheet (XLS)")


# ==========================================
# EXAMPLE USAGE
# ==========================================

if __name__ == "__main__":
    # Example 1: Analyze existing XER file
    print("="*50)
    print("P6 Schedule Analyzer Demo")
    print("="*50)
    
    # If you have a sample XER file:
    # analyzer = P6ScheduleAnalyzer("sample.xer")
    # analyzer.print_dcma_report()
    # analyzer.export_to_csv("activities.csv")
    
    print("\nTo analyze a P6 XER file:")
    print("  from p6_automation import P6ScheduleAnalyzer")
    print("  analyzer = P6ScheduleAnalyzer('your_file.xer')")
    print("  analyzer.print_dcma_report()")
    
    # Example 2: Create schedule data for P6 import
    print("\n" + "="*50)
    print("P6 Schedule Creator Demo")
    print("="*50)
    
    creator = P6ScheduleCreator("Sample Project", "2026-02-01")
    
    # Add WBS activities
    creator.add_activity("A1000", "Project Initiation", 0, "1.0")
    creator.add_activity("A1010", "Define Scope", 5, "1.1")
    creator.add_activity("A1020", "Stakeholder Analysis", 3, "1.2")
    creator.add_activity("A1030", "Project Charter", 2, "1.3")
    creator.add_activity("A2000", "Planning", 0, "2.0")
    creator.add_activity("A2010", "Create WBS", 4, "2.1")
    creator.add_activity("A2020", "Develop Schedule", 5, "2.2")
    
    # Add relationships
    creator.add_relationship("A1010", "A1020", "FS")
    creator.add_relationship("A1020", "A1030", "FS")
    creator.add_relationship("A1030", "A2010", "FS")
    creator.add_relationship("A2010", "A2020", "FS")
    
    # Add resources
    creator.add_resource("R1", "Project Manager", "Labor")
    creator.add_resource("R2", "Engineer", "Labor")
    
    # Export for P6 import
    creator.export_for_p6_import("D:/P6_Import")
    
    print("\n✓ Demo complete!")
