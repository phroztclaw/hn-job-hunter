import requests
import json
import argparse
import sys
import csv
from datetime import datetime

# HN API endpoints
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"

def get_latest_hiring_thread():
    # Get user 'whoishiring' submissions
    print("Fetching submissions from 'whoishiring'...")
    try:
        r = requests.get(f"{HN_API_BASE}/user/whoishiring.json")
        user_data = r.json()
        submission_ids = user_data.get("submitted", [])
        
        # Check the first few submissions for the latest "Who is hiring?" thread
        for sid in submission_ids[:5]:
            item = requests.get(f"{HN_API_BASE}/item/{sid}.json").json()
            if item and "title" in item and "Who is hiring" in item["title"]:
                date_str = datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d')
                print(f"Found thread: {item['title']} ({date_str})")
                return item
    except Exception as e:
        print(f"Error fetching threads: {e}")
    return None

def fetch_comments(comment_ids, keywords):
    print(f"Processing {len(comment_ids)} comments...")
    leads = []
    
    # Process a subset to avoid hammering the API too hard for a test
    # In production, iterate all, but maybe with a delay or batching
    limit = 200 # increased limit
    processed = 0
    
    for cid in comment_ids[:limit]:
        try:
            c = requests.get(f"{HN_API_BASE}/item/{cid}.json").json()
            if c and "text" in c:
                text = c["text"].lower()
                # Simple keyword matching
                score = sum(1 for k in keywords if k.lower() in text)
                
                if score >= 1: # Match at least 1 keyword
                    leads.append({
                        "id": cid,
                        "user": c.get("by", "anon"),
                        "text": c["text"], # Full text
                        "url": f"https://news.ycombinator.com/item?id={cid}",
                        "score": score
                    })
        except:
            continue
        processed += 1
        if processed % 50 == 0:
            print(f"Processed {processed} comments...")
            
    return leads

def save_leads(leads, filename, format="txt"):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        if format == "csv":
            writer = csv.writer(f)
            writer.writerow(["User", "URL", "Score", "Snippet"])
            for lead in leads:
                writer.writerow([lead['user'], lead['url'], lead['score'], lead['text'][:500]])
        else:
            f.write(f"JOB LEADS (Generated: {datetime.now()})\n")
            f.write("========================================\n\n")
            for lead in leads:
                f.write(f"User: {lead['user']} (Score: {lead['score']})\n")
                f.write(f"Link: {lead['url']}\n")
                f.write(f"Snippet: {lead['text'][:500]}...\n") # Truncate for readable output
                f.write("-" * 40 + "\n")
    print(f"Saved {len(leads)} leads to {filename}")

def main():
    parser = argparse.ArgumentParser(description="HN Job Hunter - Find remote gigs.")
    parser.add_argument("--keywords", type=str, default="remote,python", help="Comma-separated keywords to filter by (e.g. 'remote,python,contract')")
    parser.add_argument("--output", type=str, default="leads.txt", help="Output filename")
    parser.add_argument("--format", type=str, choices=["txt", "csv"], default="txt", help="Output format (txt or csv)")
    
    args = parser.parse_args()
    keywords = [k.strip() for k in args.keywords.split(",")]
    
    print(f"Hunting for jobs matching: {keywords}")
    
    thread = get_latest_hiring_thread()
    if not thread:
        print("No hiring thread found.")
        return

    if "kids" not in thread:
        print("Thread has no comments.")
        return

    leads = fetch_comments(thread["kids"], keywords)
    
    # Sort by relevance (score)
    leads.sort(key=lambda x: x["score"], reverse=True)
    
    save_leads(leads, args.output, args.format)
    print("Happy hunting!")

if __name__ == "__main__":
    main()
