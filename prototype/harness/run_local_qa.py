"""One local QA command, independent of the caller's working directory."""
from datetime import datetime
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

PROTOTYPE = Path(__file__).resolve().parents[1]


def main():
    report_date = datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat()
    stages = [
        ("Automated tests", ["-m", "pytest", "-q", "-p", "no:cacheprovider", "--junitxml=test_scenarios/results/automated_tests.xml"]),
        ("Scenario catalog", ["test_scenarios/build_report.py", "--date", report_date]),
        ("Agent evaluation", ["harness/evaluate.py"]),
    ]
    failed = False
    for label, arguments in stages:
        print(f"\n{label}", flush=True)
        code = subprocess.run([sys.executable, "-B", *arguments], cwd=PROTOTYPE, check=False).returncode
        failed = failed or code != 0
    print("Local QA FAILED; inspect the reports." if failed else "Local QA passed. Live OpenAI and evaluator review remain separate.")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
