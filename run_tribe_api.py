"""
TRIBE v2 Content A/B Test via HuggingFace Space API
No local GPU needed — runs on Reino0ne/tribev2 Space
"""
from gradio_client import Client
import json
import os
import time

HOOKS = {
    "A_storyteller": "Three years ago, CoComelon used to A/B test their videos in front of ten to fifteen live babies. Whichever version held attention the longest, that is the one that shipped to millions. Sounds absurd. But it worked. They became the most watched channel on YouTube. Now Meta just open sourced a model trained on eleven hundred hours of brain scans from seven hundred people. You feed it video, audio, or text. It predicts how the human brain responds. Seventy thousand data points across the cortex. No scanner needed. The next generation of content will not be tested on audiences. It will be tested on a digital twin of the human brain before a single person ever sees it.",

    "B_provocative": "What if you could test how someone's brain reacts to your content before they ever see it? No focus groups. No A/B tests. No waiting for analytics. Meta just made that real. They open sourced TRIBE v2, a model that predicts human brain activity from any video, audio, or text. Trained on seven hundred brains. Eleven hundred hours of scans. Seventy thousand data points per prediction. I ran this post through it before publishing. The version that lit up your temporal and prefrontal cortex the most? That is the one you are reading right now.",

    "C_blunt": "CoComelon tested videos on live babies. Meta just open sourced a way to test content on a digital copy of the human brain. TRIBE v2. Seven hundred brains scanned. Eleven hundred hours of data. Feed it any video, audio, or text, and it predicts your neural response across seventy thousand cortical data points. No scanner. No subjects. No waiting. I tested this post on it before you read it. Your brain was already predicted.",
}

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Connecting to Reino0ne/tribev2 Space...")
client = Client("Reino0ne/tribev2")
print("Connected!\n")

for name, text in HOOKS.items():
    print(f"{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")

    start = time.time()

    # Reset state between runs
    try:
        client.predict(api_name="/reset_for_new_run")
    except Exception:
        pass

    # Run prediction
    result = client.predict(
        text=text,
        api_name="/process_text",
    )
    elapsed = time.time() - start
    print(f"  Completed in {elapsed:.1f}s")
    print(f"  Result: {len(result)} items")

    for i, r in enumerate(result):
        rtype = type(r).__name__
        # Save files
        if isinstance(r, str) and (r.endswith(".png") or r.endswith(".html") or r.endswith(".json")):
            ext = r.split(".")[-1]
            dest = f"{OUTPUT_DIR}/{name}_output_{i}.{ext}"
            os.system(f"cp '{r}' '{dest}'")
            print(f"  [{i}] Saved file: {dest}")
        elif isinstance(r, dict):
            dest = f"{OUTPUT_DIR}/{name}_plot_{i}.json"
            with open(dest, "w") as f:
                json.dump(r, f)
            print(f"  [{i}] Saved plot data: {dest}")
        else:
            dest = f"{OUTPUT_DIR}/{name}_data_{i}.txt"
            with open(dest, "w") as f:
                f.write(str(r))
            print(f"  [{i}] Saved: {dest}")
            print(f"       Preview: {str(r)[:200]}")

    print()

print("="*60)
print("ALL HOOKS COMPLETE! Check the results/ directory.")
print("="*60)
