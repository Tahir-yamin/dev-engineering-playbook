#!/usr/bin/env python3
"""
Visual Quality Gate v1.0
Automated visual regression testing using Playwright and Pillow.
"""

import sys
import json
import os
import argparse
from datetime import datetime
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

def compare_images(baseline_path, current_path, diff_path, threshold=0.1):
    """
    Compare two images and return a similarity score.
    Returns: (diff_percent, is_pass)
    """
    img1 = Image.open(baseline_path).convert('RGB')
    img2 = Image.open(current_path).convert('RGB')
    
    # Ensure they are the same size
    if img1.size != img2.size:
        return 100.0, False, "Size mismatch: {} vs {}".format(img1.size, img2.size)
        
    diff = ImageChops.difference(img1, img2)
    stat = ImageStat.Stat(diff)
    
    # Calculate difference as percentage
    diff_sum = sum(stat.mean)
    diff_percent = (diff_sum / (255 * 3)) * 100
    
    is_pass = diff_percent <= threshold
    
    if not is_pass:
        diff.save(diff_path)
        
    return diff_percent, is_pass, None

def run_visual_gate(url, name, baseline_dir, results_dir, update_baseline=False):
    baseline_path = os.path.join(baseline_dir, f"{name}.png")
    current_path = os.path.join(results_dir, f"{name}_current.png")
    diff_path = os.path.join(results_dir, f"{name}_diff.png")
    
    result = {
        "url": url,
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url, wait_until="networkidle")
            
            # Allow some time for animations
            page.wait_for_timeout(1000)
            
            if update_baseline or not os.path.exists(baseline_path):
                page.screenshot(path=baseline_path, full_page=True)
                result["status"] = "baseline_created"
                result["baseline_path"] = baseline_path
            else:
                page.screenshot(path=current_path, full_page=True)
                diff_percent, is_pass, error = compare_images(baseline_path, current_path, diff_path)
                
                result["diff_percent"] = diff_percent
                result["pass"] = is_pass
                if is_pass:
                    result["status"] = "pass"
                else:
                    result["status"] = "fail"
                    result["diff_path"] = diff_path
                    result["error"] = error
            
            browser.close()
            
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual Quality Gate")
    parser.add_argument("url", help="URL to test")
    parser.add_argument("--name", required=True, help="Test name (used for filenames)")
    parser.add_argument("--baseline-dir", default="d:/my-dev-knowledge-base/tests/visual/baselines", help="Directory for baseline images")
    parser.add_argument("--results-dir", default="d:/my-dev-knowledge-base/tests/visual/results", help="Directory for test results")
    parser.add_argument("--update", action="store_true", help="Update baseline image")
    
    args = parser.parse_args()
    
    os.makedirs(args.baseline_dir, exist_ok=True)
    os.makedirs(args.results_dir, exist_ok=True)
    
    res = run_visual_gate(args.url, args.name, args.baseline_dir, args.results_dir, args.update)
    print(json.dumps(res, indent=2))
