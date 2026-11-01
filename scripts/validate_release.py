from __future__ import annotations

from pathlib import Path
import compileall
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    print("+", " ".join(map(str, cmd)))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)
    if p.stdout:
        print(p.stdout, end="")
    if p.stderr:
        print(p.stderr, end="", file=sys.stderr)
    if p.returncode != 0:
        raise SystemExit(p.returncode)

def audit_text():
    local_path_patterns = [
        re.compile(r"/mnt/[a-zA-Z]/"),
        re.compile(r"/home/[A-Za-z0-9_.-]+/"),
        re.compile(r"[A-Za-z]:\\\\"),
    ]
    secret_patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ]
    internal_patterns = [
        re.compile(r"\bRC\d", re.I),
        re.compile(r"\bPASS_[A-Z0-9_]+"),
        re.compile(r"\bNO_GO\b"),
        re.compile(r"\btruth[-_ ]unseal", re.I),
        re.compile(r"\bpost[-_ ]truth", re.I),
    ]

    local_hits = []
    secret_hits = []
    internal_hits = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix.lower() in {".png",".jpg",".jpeg",".pdf",".zip",".pyc",".log"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for rx in local_path_patterns:
            for m in rx.finditer(text):
                local_hits.append((str(p.relative_to(ROOT)), m.group(0)))
        for rx in secret_patterns:
            for m in rx.finditer(text):
                secret_hits.append((str(p.relative_to(ROOT)), m.group(0)[:32]))
        for rx in internal_patterns:
            for m in rx.finditer(text):
                internal_hits.append((str(p.relative_to(ROOT)), m.group(0)))

    # The validator source itself necessarily contains the audit regex strings.
    local_hits = [h for h in local_hits if h[0] != "scripts/validate_release.py"]
    secret_hits = [h for h in secret_hits if h[0] != "scripts/validate_release.py"]
    internal_hits = [h for h in internal_hits if h[0] != "scripts/validate_release.py"]

    return local_hits, secret_hits, internal_hits

def main():
    print("===== Graph-VALID public release validation =====")
    ok = compileall.compile_dir(ROOT / "src", quiet=1)
    ok = compileall.compile_dir(ROOT / "scripts", quiet=1) and ok
    ok = compileall.compile_dir(ROOT / "tests", quiet=1) and ok
    if not ok:
        raise SystemExit("compileall failed")
    print("compileall: PASS")

    run([sys.executable, "-m", "pytest", "-q"])
    print("pytest: PASS")

    run([sys.executable, "scripts/run_example.py"])
    print("example: PASS")

    local_hits, secret_hits, internal_hits = audit_text()
    print("absolute_local_path_hits:", len(local_hits))
    print("secret_pattern_hits:", len(secret_hits))
    print("internal_stage_pattern_hits:", len(internal_hits))
    if local_hits:
        print(json.dumps(local_hits, indent=2))
    if secret_hits:
        print(json.dumps(secret_hits, indent=2))
    if internal_hits:
        print(json.dumps(internal_hits, indent=2))
    if local_hits or secret_hits or internal_hits:
        raise SystemExit("text audit failed")

    print("text audit: PASS")

    # PUBLIC_RELEASE_DYNAMIC_VALIDATION_STATUS
    _status_path = ROOT / "VALIDATION_STATUS.json"
    _status_obj = json.loads(_status_path.read_text(encoding="utf-8"))
    print("validation_status:", _status_obj.get("status", "unknown"))
    _full = _status_obj.get("full_data_reproduction", {})
    print("full_data_reproduction_status:", _full.get("status", "unknown"))
    if _full.get("status") == "validated_against_hash_verified_canonical_outputs":
        print("full_data_reproduction_replicates:", _full.get("replicate_count", "unknown"))
        print("full_data_prediction_mismatches:", _full.get("B1_B5_rowwise_prediction_mismatches", "unknown"))
        print("full_data_intermediate_mismatches:", _full.get("B5_intermediate_mismatches", "unknown"))
        print("full_data_classwise_mismatches:", _full.get("classwise_metric_field_mismatches", "unknown"))

if __name__ == "__main__":
    main()
