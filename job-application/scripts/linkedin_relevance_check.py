"""
LinkedIn Relevance Checker (Tiny Model Edition)
===============================================
Filters scraped LinkedIn posts using semantic embeddings.
Uses 'all-MiniLM-L6-v2' (Tiny Model ~80MB) for CPU-efficient matching.

Dependencies:
    pip install sentence-transformers pyyaml
"""

import json
import os
import yaml
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_FILE = os.path.join(BASE_DIR, "config", "user_job_profile.yaml")
INPUT_FILE = os.path.join(DATA_DIR, "linkedin_posts_jobs.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "relevant_linkedin_feed.json")

def load_config():
    """Load user job profile targets."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def load_feed():
    """Load raw scraped feed."""
    if not os.path.exists(INPUT_FILE):
        print(f"⚠️ Input file not found: {INPUT_FILE}. Run scraper first.")
        return []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_relevance(feed_items, targets, model, threshold=0.45):
    """
    Calculate semantic similarity between Feed Items and Target Descriptions.
    """
    if not feed_items:
        return []

    print(f"🧠 Encoding {len(feed_items)} feed items...")
    
    # Prepare text for embedding
    # Combine Title + Description for better context
    feed_texts = [f"{item.get('role', '')} {item.get('post_text', '')}" for item in feed_items]
    target_texts = [t["description"] for t in targets["targets"]]
    
    # Encode
    feed_embeddings = model.encode(feed_texts, convert_to_tensor=True)
    target_embeddings = model.encode(target_texts, convert_to_tensor=True)
    
    # Compute Cosine Similarity
    # Result -> Matrix [num_targets, num_feed_items]
    cosine_scores = util.cos_sim(target_embeddings, feed_embeddings)
    
    relevant_items = []
    
    print("\n🔍 Checking Relevance:")
    
    for i, item in enumerate(feed_items):
        # max score across all targets
        max_score = float(cosine_scores[:, i].max())
        
        # Find which target matched best
        best_target_idx = int(cosine_scores[:, i].argmax())
        matched_target = targets["targets"][best_target_idx]["title"]
        
        if max_score >= threshold:
            item["relevance_score"] = round(max_score, 3)
            item["matched_target"] = matched_target
            relevant_items.append(item)
            print(f"  ✅ [Score: {max_score:.2f}] {item['role']} -> Matches '{matched_target}'")
        else:
            # Uncomment for debug
            # print(f"  ❌ [Score: {max_score:.2f}] {item['role']}")
            pass
            
    # Sort by score descending
    relevant_items.sort(key=lambda x: x["relevance_score"], reverse=True)
    return relevant_items

def generate_html_report(items, filename):
    """Generate a clean HTML table for the user."""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #0073b1; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .score { font-weight: bold; color: green; }
            .post-text { font-size: 0.9em; color: #555; }
            .post-link { color: #0073b1; text-decoration: none; font-weight: bold; }
            .post-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h2>🎯 LinkedIn Daily Job Report (Relevant Matches)</h2>
        <p>Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
        <table>
            <tr>
                <th>Score</th>
                <th>Role</th>
                <th>Company</th>
                <th>Location</th>
                <th>Post Link</th>
                <th>Snippet</th>
            </tr>
    """
    
    for item in items:
        post_url = item.get('post_url', 'N/A')
        post_link = f'<a href="{post_url}" target="_blank" class="post-link">View Post</a>' if post_url != "N/A" else "N/A"
        
        html += f"""
            <tr>
                <td class="score">{item['relevance_score']}</td>
                <td>{item['role']}</td>
                <td>{item['company']}</td>
                <td>{item['location']}</td>
                <td>{post_link}</td>
                <td><p class="post-text">{item['post_text'][:300]}...</p></td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📊 HTML Report Generated: {filename}")

def main():
    print("🚀 Starting LinkedIn Relevance Check (Tiny Model)...")
    
    # 1. Load Data
    config = load_config()
    feed = load_feed()
    
    if not feed:
        print("❌ No feed data to process.")
        return

    # 2. Load Model
    print("📥 Loading Tiny Model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 3. Process
    relevant_feed = calculate_relevance(feed, config, model, threshold=config.get("threshold", 0.4))
    
    # 4. Save JSON
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(relevant_feed, f, indent=2, ensure_ascii=False)
        
    # 5. Generate HTML View
    html_file = os.path.join(DATA_DIR, "daily_job_report.html")
    generate_html_report(relevant_feed, html_file)
        
    print(f"\n🎉 Done! Found {len(relevant_feed)} relevant posts.")
    print(f"📄 JSON Saved: {OUTPUT_FILE}")
    print(f"🌍 View Report: {html_file}")

if __name__ == "__main__":
    main()
