# -*- coding: utf-8 -*-
"""
Generate visual charts from code smell analysis results
"""

import json
from pathlib import Path
from collections import defaultdict


def load_latest_comparison():
    """Load the most recent comparison JSON file"""
    results_dir = Path("results")
    json_files = sorted(results_dir.glob("comparison_*.json"), reverse=True)
    
    if not json_files:
        print("No comparison files found!")
        return None
    
    latest_file = json_files[0]
    print(f"Loading: {latest_file}")
    
    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)


def print_ascii_bar_chart(title, data, max_width=50):
    """Print a simple ASCII bar chart"""
    print(f"\n{title}")
    print("=" * 60)
    
    if not data:
        print("No data available")
        return
    
    # Find max value for scaling
    max_value = max(data.values()) if data else 1
    
    for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
        bar = "#" * bar_length
        percentage = (value / sum(data.values()) * 100) if sum(data.values()) > 0 else 0
        print(f"{label:30s} {bar:50s} {value:3d} ({percentage:.1f}%)")


def generate_summary_report(comparison):
    """Generate a text-based summary report"""
    print("\n" + "="*70)
    print(" CODE SMELLS ANALYSIS - SUMMARY REPORT")
    print("="*70)
    
    # Model comparison
    print("\n[MODEL PERFORMANCE COMPARISON]")
    print("-" * 70)
    
    model_data = {}
    for model, stats in comparison["model_statistics"].items():
        model_name = model.split("/")[-1].split(":")[0][:20]
        model_data[model_name] = stats["total_smells_found"]
    
    print_ascii_bar_chart("Total Smells Found by Model", model_data)
    
    # Release evolution
    print("\n\n[EVOLUTION BY RELEASE]")
    print("-" * 70)
    
    release_data = {}
    for release, stats in comparison.get("release_statistics", {}).items():
        release_data[release] = stats["total_smells_found"]
    
    print_ascii_bar_chart("Total Smells by Release", release_data)
    
    # Top code smells
    print("\n\n[TOP CODE SMELLS - ALL RELEASES]")
    print("-" * 70)
    
    all_smells = defaultdict(int)
    for release, stats in comparison.get("release_statistics", {}).items():
        for smell, count in stats["smell_types_distribution"].items():
            all_smells[smell] += count
    
    print_ascii_bar_chart("Most Frequent Code Smells", dict(all_smells))
    
    # Severity distribution
    print("\n\n[SEVERITY DISTRIBUTION BY MODEL]")
    print("-" * 70)
    
    for model, stats in comparison["model_statistics"].items():
        model_name = model.split("/")[-1].split(":")[0]
        print(f"\n{model_name}:")
        severity_data = stats.get("severity_distribution", {})
        
        if severity_data:
            total = sum(severity_data.values())
            for severity in ["High", "Medium", "Low"]:
                count = severity_data.get(severity, 0)
                percentage = (count / total * 100) if total > 0 else 0
                bar_length = int(percentage / 2)  # Scale to 50 chars max
                bar = "#" * bar_length
                print(f"  {severity:8s} {bar:50s} {count:3d} ({percentage:.1f}%)")
    
    # Consensus smells
    print("\n\n[HIGH-CONFIDENCE CODE SMELLS - CONSENSUS]")
    print("-" * 70)
    
    consensus = comparison.get("consensus_smells", [])
    if consensus:
        print(f"\nFound {len(consensus)} code smells detected by multiple models:\n")
        for smell in sorted(consensus, key=lambda x: x["agreement_count"], reverse=True):
            print(f"  * {smell['smell_type']:25s} in {smell['file']}")
            print(f"    Location: {smell['location'].get('function', 'N/A')}")
            print(f"    Agreement: {smell['agreement_count']} models\n")
    else:
        print("\nNo consensus smells found (detected by multiple models)")
    
    # Key insights
    print("\n\n[KEY INSIGHTS]")
    print("-" * 70)
    
    total_files = comparison.get("total_files_analyzed", 0)
    total_smells = sum(stats["total_smells_found"] for stats in comparison["model_statistics"].values())
    avg_smells = total_smells / len(comparison["model_statistics"]) if comparison["model_statistics"] else 0
    
    print(f"\n  Total files analyzed: {total_files}")
    print(f"  Total smells detected: {total_smells}")
    print(f"  Average per model: {avg_smells:.1f}")
    
    # Release trend
    release_stats = comparison.get("release_statistics", {})
    if len(release_stats) > 1:
        releases_sorted = sorted(release_stats.items())
        first_release = releases_sorted[0][1]["total_smells_found"]
        last_release = releases_sorted[-1][1]["total_smells_found"]
        
        if first_release > 0:
            improvement = ((first_release - last_release) / first_release) * 100
            trend = "IMPROVED" if improvement > 0 else "DEGRADED"
            print(f"\n  Quality trend: {trend}")
            print(f"  Change: {abs(improvement):.1f}% {'reduction' if improvement > 0 else 'increase'}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main function"""
    comparison = load_latest_comparison()
    
    if not comparison:
        return
    
    generate_summary_report(comparison)
    
    print("Run 'python generate_charts.py > results/visual_summary.txt' to save output")


if __name__ == "__main__":
    main()
