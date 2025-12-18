# -*- coding: utf-8 -*-
"""
Code Smells Detection System using HuggingFace LLM Models

This script analyzes Python code using 3 different HuggingFace models
to detect code smells based on: https://refactoring.guru/refactoring/smells
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


# HuggingFace Models Configuration
MODELS = [
    "Qwen/Qwen2.5-7B-Instruct",
    "google/gemma-2-2b-it:nebius",
    "openai/gpt-oss-120b:groq",
]

API_URL = "https://router.huggingface.co/v1/chat/completions"

# Complete list of code smells from Refactoring Guru
CODE_SMELLS = {
    "Bloaters": [
        "Long Method",
        "Large Class",
        "Primitive Obsession",
        "Long Parameter List",
        "Data Clumps",
    ],
    "Object-Orientation Abusers": [
        "Switch Statements",
        "Temporary Field",
        "Refused Bequest",
        "Alternative Classes with Different Interfaces",
    ],
    "Change Preventers": [
        "Divergent Change",
        "Shotgun Surgery",
        "Parallel Inheritance Hierarchies",
    ],
    "Dispensables": [
        "Comments",
        "Duplicate Code",
        "Lazy Class",
        "Data Class",
        "Dead Code",
        "Speculative Generality",
    ],
    "Couplers": [
        "Feature Envy",
        "Inappropriate Intimacy",
        "Message Chains",
        "Middle Man",
    ],
}

SYSTEM_PROMPT = """You are an expert Software Engineer specialized in code quality analysis and refactoring.

Your task is to analyze Python code and identify CODE SMELLS based on the Refactoring Guru taxonomy.

Focus on these categories:
1. BLOATERS: Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps
2. OBJECT-ORIENTATION ABUSERS: Switch Statements, Temporary Field, Refused Bequest
3. CHANGE PREVENTERS: Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies
4. DISPENSABLES: Comments, Duplicate Code, Lazy Class, Data Class, Dead Code, Speculative Generality
5. COUPLERS: Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man

For EACH code smell found, provide:
- smell_type: The exact name of the code smell
- category: Which category it belongs to (Bloaters, Object-Orientation Abusers, etc.)
- location: File path, line numbers, function/class name
- evidence: Specific code snippet showing the problem
- severity: Low, Medium, or High
- justification: Technical explanation of why this is a problem
- refactoring_suggestion: Concrete steps to fix it
- refactored_example: Short code example showing the improved version

Return your analysis in JSON format with this structure:
{
  "file_analyzed": "path/to/file.py",
  "total_smells_found": 5,
  "smells": [
    {
      "smell_type": "Long Method",
      "category": "Bloaters",
      "location": {
        "file": "path/to/file.py",
        "line_start": 10,
        "line_end": 150,
        "function": "process_data",
        "class": "DataProcessor"
      },
      "evidence": "def process_data():\\n    # 140 lines of code...",
      "severity": "High",
      "justification": "Method has 140 lines, exceeding recommended 20-30 lines...",
      "refactoring_suggestion": "Extract smaller methods: validate_input(), transform_data(), save_result()",
      "refactored_example": "def process_data():\\n    data = validate_input()\\n    result = transform_data(data)\\n    save_result(result)"
    }
  ]
}

Be thorough but precise. Only report actual code smells with concrete evidence."""


class CodeSmellAnalyzer:
    """Analyzes code using multiple HuggingFace LLM models"""

    def __init__(self, models: List[str]):
        self.models = models
        self.api_url = API_URL
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}",
            "Content-Type": "application/json",
        }
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

    def query_model(self, model: str, code: str, file_path: str) -> Dict[str, Any]:
        """
        Query HuggingFace model for code smell analysis

        Args:
            model: HuggingFace model name
            code: Python code to analyze
            file_path: Path of the file being analyzed

        Returns:
            Model response in JSON format
        """
        user_prompt = f"""Analyze this Python code for code smells:

FILE: {file_path}

```python
{code}
```

Provide a comprehensive analysis in JSON format as specified."""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"},
        }

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=payload, timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Try to parse as JSON
            try:
                parsed_content = json.loads(content)
                return {
                    "success": True,
                    "model": model,
                    "file": file_path,
                    "analysis": parsed_content,
                    "raw_response": content,
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "model": model,
                    "file": file_path,
                    "error": "Failed to parse JSON response",
                    "raw_response": content,
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "model": model,
                "file": file_path,
                "error": str(e),
            }

    def read_python_files(
        self, directory: Path, max_size: int = 50000
    ) -> List[Dict[str, str]]:
        """
        Read all Python files from a directory recursively

        Args:
            directory: Root directory to search
            max_size: Maximum file size in characters

        Returns:
            List of dictionaries with path and content
        """
        python_files = []

        for py_file in directory.rglob("*.py"):
            try:
                # Ignore test files and cache
                if any(
                    skip in str(py_file)
                    for skip in ["__pycache__", "test_", "_test.py", ".pyc"]
                ):
                    continue

                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Limit file size
                if len(content) > max_size:
                    print(
                        f"Warning: Large file truncated: {py_file} ({len(content)} chars)"
                    )
                    content = content[:max_size]

                relative_path = py_file.relative_to(directory)

                # Extract release version from path
                parts = relative_path.parts
                release_version = parts[0] if parts else "unknown"

                python_files.append(
                    {
                        "path": str(relative_path),
                        "full_path": str(py_file),
                        "content": content,
                        "size": len(content),
                        "release": release_version,
                    }
                )

            except Exception as e:
                print(f"Error reading {py_file}: {e}")
                continue

        return python_files

    def sample_files_balanced(
        self, python_files: List[Dict[str, str]], sample_size: int
    ) -> List[Dict[str, str]]:
        """
        Sample files in a balanced way across all releases

        Args:
            python_files: List of all Python files
            sample_size: Total number of files to sample

        Returns:
            Balanced sample of files from all releases
        """
        from collections import defaultdict

        # Group files by release
        files_by_release = defaultdict(list)
        for file_info in python_files:
            release = file_info.get("release", "unknown")
            files_by_release[release].append(file_info)

        releases = sorted(files_by_release.keys())
        num_releases = len(releases)

        if num_releases == 0:
            return []

        # Calculate files per release (balanced)
        files_per_release = sample_size // num_releases
        remainder = sample_size % num_releases

        sampled_files = []

        print(f"\nBalanced sampling across {num_releases} releases:")

        for idx, release in enumerate(releases):
            available = files_by_release[release]
            # Add one extra file to first 'remainder' releases to distribute the remainder
            target = files_per_release + (1 if idx < remainder else 0)
            # Don't sample more than available
            count = min(target, len(available))

            sampled = available[:count]
            sampled_files.extend(sampled)

            print(
                f"  Release {release}: {count} files (out of {len(available)} available)"
            )

        return sampled_files

    def analyze_file_with_models(
        self, file_info: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        Analyze a file with all configured models

        Args:
            file_info: Dictionary with file information

        Returns:
            List of results from each model
        """
        results = []

        print(f"\nAnalyzing: {file_info['path']}")
        print(f"   Size: {file_info['size']} characters")

        for model in self.models:
            print(f"   Model: {model}")

            result = self.query_model(
                model=model, code=file_info["content"], file_path=file_info["path"]
            )

            results.append(result)

            if result["success"]:
                smells_found = result.get("analysis", {}).get("total_smells_found", 0)
                print(f"      Success: {smells_found} code smells found")
            else:
                print(f"      Error: {result.get('error', 'Unknown error')}")

        return results

    def save_results(self, all_results: List[Dict[str, Any]], timestamp: str):
        """
        Save all analysis results

        Args:
            all_results: List with all results
            timestamp: Execution timestamp
        """
        output_file = self.results_dir / f"analysis_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_file}")

    def compare_models(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare results between different models

        Args:
            all_results: List with results from all models

        Returns:
            Dictionary with statistical comparison
        """
        comparison = {
            "models_compared": self.models,
            "total_files_analyzed": 0,
            "model_statistics": {},
            "consensus_smells": [],
            "unique_smells": {},
            "agreement_matrix": {},
        }

        # Statistics per model
        for model in self.models:
            model_results = [
                r for r in all_results if r.get("model") == model and r.get("success")
            ]

            total_smells = 0
            smell_types = defaultdict(int)
            severity_counts = defaultdict(int)

            for result in model_results:
                analysis = result.get("analysis", {})
                if not isinstance(analysis, dict):
                    continue
                smells = analysis.get("smells", [])
                if not isinstance(smells, list):
                    continue
                total_smells += len(smells)

                for smell in smells:
                    if not isinstance(smell, dict):
                        continue
                    smell_types[smell.get("smell_type", "Unknown")] += 1
                    severity_counts[smell.get("severity", "Unknown")] += 1

            comparison["model_statistics"][model] = {
                "files_analyzed": len(model_results),
                "total_smells_found": total_smells,
                "avg_smells_per_file": total_smells / len(model_results)
                if model_results
                else 0,
                "smell_types_distribution": dict(smell_types),
                "severity_distribution": dict(severity_counts),
            }

        # Statistics per release
        release_statistics = {}
        successful_results = [r for r in all_results if r.get("success")]

        # Extract release from file path
        releases_found = set()
        for result in successful_results:
            file_path = result.get("file", "")
            if "/" in file_path or "\\" in file_path:
                release = file_path.split("/")[0].split("\\")[0]
                releases_found.add(release)

        for release in sorted(releases_found):
            release_results = [
                r
                for r in successful_results
                if r.get("file", "").startswith(release + "/")
                or r.get("file", "").startswith(release + "\\")
            ]

            total_smells = 0
            smell_types = defaultdict(int)

            for result in release_results:
                analysis = result.get("analysis", {})
                if not isinstance(analysis, dict):
                    continue
                smells = analysis.get("smells", [])
                if not isinstance(smells, list):
                    continue

                for smell in smells:
                    if not isinstance(smell, dict):
                        continue
                    total_smells += 1
                    smell_types[smell.get("smell_type", "Unknown")] += 1

            files_in_release = len(
                set(r.get("file") for r in release_results if r.get("success"))
            )

            release_statistics[release] = {
                "files_analyzed": files_in_release,
                "total_smells_found": total_smells,
                "avg_smells_per_file": total_smells / files_in_release
                if files_in_release
                else 0,
                "smell_types_distribution": dict(smell_types),
            }

        comparison["release_statistics"] = release_statistics

        # Find code smells identified by multiple models (consensus)
        files_analyzed = set(r.get("file") for r in all_results if r.get("success"))
        comparison["total_files_analyzed"] = len(files_analyzed)

        for file_path in files_analyzed:
            file_results = [
                r
                for r in all_results
                if r.get("file") == file_path and r.get("success")
            ]

            if len(file_results) < 2:
                continue

            # Group smells by type and location
            smells_by_type = defaultdict(list)

            for result in file_results:
                analysis = result.get("analysis", {})
                if not isinstance(analysis, dict):
                    continue
                smells = analysis.get("smells", [])
                if not isinstance(smells, list):
                    continue
                for smell in smells:
                    if not isinstance(smell, dict):
                        continue
                    # Safely extract location information
                    location = smell.get("location", {})
                    if not isinstance(location, dict):
                        location = {}

                    # Create hashable key from smell type and location
                    smell_type = smell.get("smell_type", "Unknown")
                    function_name = location.get("function", None)
                    class_name = location.get("class", None)

                    # Ensure all key components are hashable (strings or None)
                    if isinstance(function_name, list):
                        function_name = str(function_name)
                    if isinstance(class_name, list):
                        class_name = str(class_name)

                    key = (smell_type, function_name, class_name)
                    smells_by_type[key].append(
                        {"model": result["model"], "smell": smell}
                    )

            # Smells found by more than one model
            for key, detections in smells_by_type.items():
                if len(detections) >= 2:
                    comparison["consensus_smells"].append(
                        {
                            "file": file_path,
                            "smell_type": key[0],
                            "location": {"function": key[1], "class": key[2]},
                            "detected_by": [d["model"] for d in detections],
                            "agreement_count": len(detections),
                        }
                    )

        return comparison

    def generate_report(self, comparison: Dict[str, Any], timestamp: str):
        """
        Generate readable comparison report

        Args:
            comparison: Comparison data between models
            timestamp: Execution timestamp
        """
        report_file = self.results_dir / f"report_{timestamp}.txt"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("CODE SMELLS ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Models analyzed: {len(comparison['models_compared'])}\n")
            f.write(f"Files analyzed: {comparison['total_files_analyzed']}\n\n")

            f.write("-" * 80 + "\n")
            f.write("STATISTICS PER MODEL\n")
            f.write("-" * 80 + "\n\n")

            for model, stats in comparison["model_statistics"].items():
                f.write(f"Model: {model}\n")
                f.write(f"   Files: {stats['files_analyzed']}\n")
                f.write(f"   Total smells: {stats['total_smells_found']}\n")
                f.write(f"   Average per file: {stats['avg_smells_per_file']:.2f}\n")

                f.write(f"\n   Distribution by type:\n")
                for smell_type, count in sorted(
                    stats["smell_types_distribution"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                ):
                    f.write(f"      - {smell_type}: {count}\n")

                f.write(f"\n   Distribution by severity:\n")
                for severity, count in stats["severity_distribution"].items():
                    f.write(f"      - {severity}: {count}\n")

                f.write("\n")

            # Statistics per release
            if "release_statistics" in comparison and comparison["release_statistics"]:
                f.write("-" * 80 + "\n")
                f.write("STATISTICS PER RELEASE\n")
                f.write("-" * 80 + "\n\n")

                for release, stats in sorted(comparison["release_statistics"].items()):
                    f.write(f"Release: {release}\n")
                    f.write(f"   Files analyzed: {stats['files_analyzed']}\n")
                    f.write(f"   Total smells: {stats['total_smells_found']}\n")
                    f.write(
                        f"   Average per file: {stats['avg_smells_per_file']:.2f}\n"
                    )

                    f.write(f"\n   Distribution by type:\n")
                    for smell_type, count in sorted(
                        stats["smell_types_distribution"].items(),
                        key=lambda x: x[1],
                        reverse=True,
                    ):
                        f.write(f"      - {smell_type}: {count}\n")

                    f.write("\n")

            f.write("-" * 80 + "\n")
            f.write("CONSENSUS CODE SMELLS (detected by multiple models)\n")
            f.write("-" * 80 + "\n\n")

            if comparison["consensus_smells"]:
                for smell in sorted(
                    comparison["consensus_smells"],
                    key=lambda x: x["agreement_count"],
                    reverse=True,
                ):
                    f.write(f"Type: {smell['smell_type']}\n")
                    f.write(f"   File: {smell['file']}\n")
                    f.write(f"   Location: {smell['location']}\n")
                    f.write(
                        f"   Detected by {smell['agreement_count']} models: {', '.join(smell['detected_by'])}\n\n"
                    )
            else:
                f.write("No code smells detected by multiple models.\n\n")

            f.write("=" * 80 + "\n")

        print(f"Report generated: {report_file}")

    def run_analysis(self, releases_dir: Path, sample_size: int = None):
        """
        Execute complete analysis of releases directory

        Args:
            releases_dir: Path to releases folder
            sample_size: Maximum number of files to analyze (None = all)
        """
        print("=" * 80)
        print("CODE SMELLS ANALYSIS STARTED")
        print("=" * 80)

        # Check token
        if not os.environ.get("HF_TOKEN"):
            print("WARNING: HF_TOKEN not found in environment variables")
            print("   Set with: export HF_TOKEN=your_token_here")

        # Timestamp for this execution
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Read Python files
        print(f"\nReading Python files from: {releases_dir}")
        python_files = self.read_python_files(releases_dir)

        if not python_files:
            print("ERROR: No Python files found!")
            return

        print(f"Found {len(python_files)} Python files")

        # Limit sample if necessary with balanced sampling across releases
        if sample_size and len(python_files) > sample_size:
            print(f"\nLimiting analysis to {sample_size} files (balanced sample)")
            python_files = self.sample_files_balanced(python_files, sample_size)
        else:
            # Show release distribution even when analyzing all files
            from collections import defaultdict

            files_by_release = defaultdict(int)
            for file_info in python_files:
                release = file_info.get("release", "unknown")
                files_by_release[release] += 1

            print(f"\nFiles per release:")
            for release in sorted(files_by_release.keys()):
                print(f"  Release {release}: {files_by_release[release]} files")

        # Analyze each file with all models
        all_results = []

        for idx, file_info in enumerate(python_files, 1):
            print(f"\n[{idx}/{len(python_files)}]")
            file_results = self.analyze_file_with_models(file_info)
            all_results.extend(file_results)

        # Save raw results
        self.save_results(all_results, timestamp)

        # Compare models
        print("\n" + "=" * 80)
        print("COMPARING RESULTS BETWEEN MODELS")
        print("=" * 80)

        comparison = self.compare_models(all_results)

        # Save comparison
        comparison_file = self.results_dir / f"comparison_{timestamp}.json"
        with open(comparison_file, "w", encoding="utf-8") as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)

        print(f"Comparison saved to: {comparison_file}")

        # Generate report
        self.generate_report(comparison, timestamp)

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETED")
        print("=" * 80)


def main():
    """Main function"""

    # Configure paths
    releases_dir = Path("releases")

    if not releases_dir.exists():
        print(f"ERROR: Directory not found: {releases_dir}")
        return

    # Create analyzer
    analyzer = CodeSmellAnalyzer(models=MODELS)

    # Execute analysis
    # Use sample_size to limit number of files (useful for testing)
    analyzer.run_analysis(
        releases_dir=releases_dir,
        sample_size=5,  # Remove or adjust to analyze all files
    )


if __name__ == "__main__":
    main()
