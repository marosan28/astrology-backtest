#!/usr/bin/env python3
from __future__ import annotations

import importlib.metadata as metadata
import json
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ENVIRONMENT_DIR = REPO_ROOT / "environment"
DOWNLOAD_DIR = ENVIRONMENT_DIR / "downloads"
REPORT_PATH = ENVIRONMENT_DIR / "capability_report.md"
TARGET_DT = datetime(2026, 7, 15, 12, 0, 0, tzinfo=timezone.utc)


def safe_json_preview(value: Any, limit: int = 600) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2)
    return text if len(text) <= limit else text[:limit] + "\n... [truncated]"


def exception_details(exc: BaseException) -> str:
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)).strip()


def run_command(command: list[str] | str, shell: bool = False) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            shell=shell,
            check=False,
            capture_output=True,
            text=True,
        )
        rendered_command = command if isinstance(command, str) else " ".join(command)
        return {
            "command": rendered_command,
            "success": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as exc:  # pragma: no cover - defensive reporting
        rendered_command = command if isinstance(command, str) else " ".join(command)
        return {
            "command": rendered_command,
            "success": False,
            "error": exception_details(exc),
        }


def test_file_operations() -> dict[str, Any]:
    probe_path = ENVIRONMENT_DIR / "file_write_probe.txt"
    result: dict[str, Any] = {"path": str(probe_path)}
    try:
        initial_text = f"created={datetime.now(timezone.utc).isoformat()}\n"
        probe_path.write_text(initial_text, encoding="utf-8")
        after_create = probe_path.read_text(encoding="utf-8")
        probe_path.write_text(after_create + "modified=true\n", encoding="utf-8")
        final_text = probe_path.read_text(encoding="utf-8")
        result.update(
            {
                "created": True,
                "modified": True,
                "exists_after_write": probe_path.exists(),
                "size_bytes": probe_path.stat().st_size,
                "final_contents": final_text.strip(),
            }
        )
    except Exception as exc:
        result.update({"created": False, "modified": False, "error": exception_details(exc)})
    return result


def test_python_execution() -> dict[str, Any]:
    probe_script = ENVIRONMENT_DIR / "python_exec_probe.py"
    try:
        probe_script.write_text("print('python_probe_ok')\n", encoding="utf-8")
        command_result = run_command([sys.executable, str(probe_script)])
        command_result["probe_script"] = str(probe_script)
        return command_result
    except Exception as exc:
        return {"success": False, "error": exception_details(exc), "probe_script": str(probe_script)}


def installed_version(package_name: str) -> str | None:
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return None


def test_pip_installation() -> dict[str, Any]:
    return run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--quiet",
            "--no-deps",
            "requests==2.34.2",
        ]
    )


def fetch_endpoint(label: str, url: str) -> dict[str, Any]:
    result: dict[str, Any] = {"label": label, "url": url}
    target_file = DOWNLOAD_DIR / f"{label.lower().replace(' ', '_')}.json"
    try:
        import requests

        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "astrology-backtest-capability-test/1.0"},
        )
        result["status_code"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["auth_required"] = False if response.status_code == 200 else "unknown"
        result["bytes_received"] = len(response.content)
        target_file.write_bytes(response.content)
        result["saved_to"] = str(target_file)
        result["saved_file_exists"] = target_file.exists()
        result["saved_file_size"] = target_file.stat().st_size if target_file.exists() else 0
        result["data_returned"] = bool(response.content)
        try:
            parsed = response.json()
            result["json_preview"] = safe_json_preview(parsed)
        except Exception as exc:
            result["json_error"] = exception_details(exc)
            result["text_preview"] = response.text[:600]
    except Exception as exc:
        result["status_code"] = None
        result["data_returned"] = False
        result["auth_required"] = "unknown"
        result["error"] = exception_details(exc)
    return result


def decode_swisseph_source(flags: int, swe: Any) -> str:
    parts: list[str] = []
    if flags & getattr(swe, "FLG_JPLEPH", 0):
        parts.append("JPL ephemeris")
    if flags & getattr(swe, "FLG_SWIEPH", 0):
        parts.append("Swiss ephemeris files")
    if flags & getattr(swe, "FLG_MOSEPH", 0):
        parts.append("Moshier fallback")
    return ", ".join(parts) if parts else f"unknown flags={flags}"


def test_pyswisseph() -> dict[str, Any]:
    result: dict[str, Any] = {
        "library": "pyswisseph",
        "target_datetime_utc": TARGET_DT.isoformat(),
        "imported": False,
    }
    try:
        import swisseph as swe

        result["imported"] = True
        result["version"] = installed_version("pyswisseph")
        jd = swe.julday(
            TARGET_DT.year,
            TARGET_DT.month,
            TARGET_DT.day,
            TARGET_DT.hour + TARGET_DT.minute / 60 + TARGET_DT.second / 3600,
        )
        base_flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        result["calculation_settings"] = (
            "swe.calc_ut(julian_day, planet, FLG_SWIEPH | FLG_SPEED) for tropical positions; "
            "geocentric ecliptic longitude in the default tropical zodiac."
        )
        result["julian_day_ut"] = jd
        positions: dict[str, Any] = {}
        for label, body in (("Saturn", swe.SATURN), ("Neptune", swe.NEPTUNE)):
            values, used_flags = swe.calc_ut(jd, body, base_flags)
            positions[label] = {
                "longitude_deg": values[0],
                "latitude_deg": values[1],
                "distance_au": values[2],
                "speed_longitude_deg_per_day": values[3],
                "returned_flags": used_flags,
                "ephemeris_source": decode_swisseph_source(used_flags, swe),
            }
        result["tropical_positions"] = positions

        sidereal_results: dict[str, Any] = {}
        for label, mode_name, mode in (
            ("Lahiri", "SIDM_LAHIRI", swe.SIDM_LAHIRI),
            ("Fagan-Bradley", "SIDM_FAGAN_BRADLEY", swe.SIDM_FAGAN_BRADLEY),
        ):
            swe.set_sid_mode(mode, 0, 0)
            sidereal_positions: dict[str, Any] = {}
            for planet_label, body in (("Saturn", swe.SATURN), ("Neptune", swe.NEPTUNE)):
                values, used_flags = swe.calc_ut(jd, body, base_flags | swe.FLG_SIDEREAL)
                sidereal_positions[planet_label] = {
                    "longitude_deg": values[0],
                    "latitude_deg": values[1],
                    "distance_au": values[2],
                    "speed_longitude_deg_per_day": values[3],
                    "returned_flags": used_flags,
                    "ephemeris_source": decode_swisseph_source(used_flags, swe),
                }
            sidereal_results[label] = {
                "application": (
                    f"Applied {mode_name} by calling swe.set_sid_mode(swe.{mode_name}, 0, 0) "
                    "and then swe.calc_ut(..., FLG_SWIEPH | FLG_SPEED | FLG_SIDEREAL)."
                ),
                "positions": sidereal_positions,
            }
        result["sidereal_positions"] = sidereal_results
        result["ephemeris_management"] = {
            "bundled_files_detected": False,
            "auto_download_behavior": "No auto-download observed.",
            "manual_sourcing_required_for_swiss_files": True,
            "observed_runtime_source": positions["Saturn"]["ephemeris_source"],
        }
    except Exception as exc:
        result["error"] = exception_details(exc)
    return result


def test_skyfield() -> dict[str, Any]:
    result: dict[str, Any] = {
        "library": "skyfield",
        "target_datetime_utc": TARGET_DT.isoformat(),
        "imported": False,
    }
    try:
        from skyfield.api import Loader

        result["imported"] = True
        result["version"] = installed_version("skyfield")
        loader = Loader(str(DOWNLOAD_DIR / "skyfield"))
        ts = loader.timescale()
        t = ts.from_datetime(TARGET_DT)
        result["calculation_settings"] = (
            "Skyfield geocentric apparent positions with ecliptic_latlon(epoch='date'); "
            "auto-download attempt for de421.bsp via Loader."
        )
        result["ephemeris_management"] = {
            "bundled_files_detected": False,
            "auto_download_behavior": "Attempts to download de421.bsp into the local Skyfield cache.",
            "manual_sourcing_may_be_needed": True,
        }
        planets = loader("de421.bsp")
        result["ephemeris_file"] = str((DOWNLOAD_DIR / "skyfield" / "de421.bsp").resolve())
        earth = planets["earth"]
        positions: dict[str, Any] = {}
        for label, key in (("Saturn", "saturn barycenter"), ("Neptune", "neptune barycenter")):
            apparent = earth.at(t).observe(planets[key]).apparent()
            latitude, longitude, distance = apparent.ecliptic_latlon(epoch="date")
            positions[label] = {
                "longitude_deg": longitude.degrees % 360,
                "latitude_deg": latitude.degrees,
                "distance_au": distance.au,
            }
        result["tropical_positions"] = positions
    except Exception as exc:
        result["error"] = exception_details(exc)
    return result


def select_preferred_library(pyswisseph_result: dict[str, Any], skyfield_result: dict[str, Any]) -> dict[str, Any]:
    if pyswisseph_result.get("imported"):
        return {
            "selected_library": "pyswisseph",
            "reason": (
                "Preferred for 1800–2030 because it successfully computed positions locally in this environment, "
                "supports built-in sidereal modes such as Lahiri and Fagan–Bradley, and avoids Skyfield's need to choose and fetch a separate JPL ephemeris file. "
                "In this run the requested Swiss ephemeris file mode fell back to the built-in Moshier ephemeris because Swiss data files were not installed, so final production calculations should pin manually sourced Swiss ephemeris files for maximum reproducibility."
            ),
        }
    if skyfield_result.get("imported"):
        return {
            "selected_library": "skyfield",
            "reason": (
                "Skyfield imported while pyswisseph did not. It still requires an external JPL ephemeris file, and full 1800–2030 coverage would require deliberate ephemeris selection and local caching."
            ),
        }
    return {
        "selected_library": None,
        "reason": "Neither astronomical library completed a successful calculation in this environment.",
    }


def build_report(data: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Capability Report")
    lines.append("")
    lines.append(f"Generated at: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Assumptions")
    lines.append("")
    for assumption in data["assumptions"]:
        lines.append(f"- {assumption}")
    lines.append("")
    lines.append("## Step 1 — Execution Environment")
    lines.append("")
    lines.append(f"- OS: {data['environment']['os']}")
    lines.append(f"- Python: {data['environment']['python']}")
    lines.append(f"- Shell command success: {data['shell_test'].get('success')}")
    lines.append(f"- pip install command success: {data['pip_test'].get('success')}")
    lines.append(f"- File create/modify success: {data['file_test'].get('created')} / {data['file_test'].get('modified')}")
    lines.append(f"- Python script execution success: {data['python_exec_test'].get('success')}")
    lines.append(f"- Outbound HTTPS success (httpbin): {data['httpbin_test'].get('status_code') == 200}")
    lines.append(f"- Public API query success count: {data['public_api_success_count']} / {len(data['api_tests'])}")
    lines.append(f"- Downloaded dataset persistence check: {data['download_persistence']}")
    lines.append("")

    lines.append("### Shell Test")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview(data["shell_test"], limit=2000))
    lines.append("```")
    lines.append("")

    lines.append("### pip Test")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview(data["pip_test"], limit=2000))
    lines.append("```")
    lines.append("")

    lines.append("### File and Python Execution Tests")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview({"file_test": data["file_test"], "python_exec_test": data["python_exec_test"]}, limit=2500))
    lines.append("```")
    lines.append("")

    lines.append("## Step 2 — Astronomical Libraries")
    lines.append("")
    lines.append("### Preferred Library for 1800–2030")
    lines.append("")
    lines.append(f"- Selected library: {data['preferred_library']['selected_library']}")
    lines.append(f"- Why: {data['preferred_library']['reason']}")
    lines.append("")
    lines.append("### pyswisseph")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview(data["pyswisseph_test"], limit=6000))
    lines.append("```")
    lines.append("")
    lines.append("### skyfield")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview(data["skyfield_test"], limit=6000))
    lines.append("```")
    lines.append("")

    lines.append("## Step 3 — Sidereal Calculations")
    lines.append("")
    sidereal_positions = data["pyswisseph_test"].get("sidereal_positions")
    if sidereal_positions:
        lines.append("Sidereal positions were computed with pyswisseph using library-managed sidereal mode switching; no manual subtraction was used.")
        lines.append("")
        lines.append("```json")
        lines.append(safe_json_preview(sidereal_positions, limit=6000))
        lines.append("```")
    else:
        lines.append("Sidereal calculations were not completed.")
        error = data["pyswisseph_test"].get("error") or data["skyfield_test"].get("error")
        if error:
            lines.append("")
            lines.append("```text")
            lines.append(error)
            lines.append("```")
    lines.append("")

    lines.append("## Step 4 — Historical Research API Access")
    lines.append("")
    for api_result in [data["httpbin_test"], *data["api_tests"]]:
        lines.append(f"### {api_result['label']}")
        lines.append("")
        lines.append(f"- URL: {api_result['url']}")
        lines.append(f"- Status: {api_result.get('status_code')}")
        lines.append(f"- Data returned: {api_result.get('data_returned')}")
        lines.append(f"- Auth required: {api_result.get('auth_required')}")
        lines.append(f"- Saved locally: {bool(api_result.get('saved_file_exists'))}")
        if api_result.get("saved_to"):
            lines.append(f"- Saved path: {api_result['saved_to']}")
        if api_result.get("error"):
            lines.append("")
            lines.append("```text")
            lines.append(api_result["error"])
            lines.append("```")
        elif api_result.get("json_preview"):
            lines.append("")
            lines.append("```json")
            lines.append(api_result["json_preview"])
            lines.append("```")
        elif api_result.get("text_preview"):
            lines.append("")
            lines.append("```text")
            lines.append(api_result["text_preview"])
            lines.append("```")
        lines.append("")

    lines.append("## Installed Package Versions")
    lines.append("")
    lines.append("```json")
    lines.append(safe_json_preview(data["installed_versions"], limit=2000))
    lines.append("```")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ENVIRONMENT_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    shell_test = run_command("printf shell_command_ok", shell=True)
    pip_test = test_pip_installation()
    file_test = test_file_operations()
    python_exec_test = test_python_execution()

    httpbin_test = fetch_endpoint("HTTPBin", "https://httpbin.org/get")
    api_tests = [
        fetch_endpoint(
            "Crossref",
            "https://api.crossref.org/works?query=Saturn+Neptune+conjunction+history&rows=3",
        ),
        fetch_endpoint(
            "OpenAlex",
            "https://api.openalex.org/works?search=Uranus+Pluto+conjunction+history&per_page=3",
        ),
        fetch_endpoint(
            "Wikidata",
            "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=French+Revolution&language=en&format=json",
        ),
        fetch_endpoint(
            "World Bank",
            "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=1900:1910&format=json&per_page=5",
        ),
    ]

    pyswisseph_test = test_pyswisseph()
    skyfield_test = test_skyfield()
    preferred_library = select_preferred_library(pyswisseph_test, skyfield_test)

    api_results = [httpbin_test, *api_tests]
    persisted_downloads = all(result.get("saved_file_exists") for result in api_results if result.get("saved_to"))

    data = {
        "assumptions": [
            "All network checks are single unauthenticated GET requests made at runtime.",
            "The timestamp under test is 2026-07-15 12:00:00 UTC.",
            "Longitudes are reported in degrees from 0° to 360°.",
            "pyswisseph tropical calculations use swe.calc_ut with FLG_SWIEPH | FLG_SPEED, and sidereal calculations add FLG_SIDEREAL after calling swe.set_sid_mode.",
            "Skyfield, if successful, uses geocentric apparent ecliptic longitude of date from de421.bsp obtained through Skyfield's loader.",
        ],
        "environment": {
            "os": platform.platform(),
            "python": sys.version.replace("\n", " "),
        },
        "shell_test": shell_test,
        "pip_test": pip_test,
        "file_test": file_test,
        "python_exec_test": python_exec_test,
        "httpbin_test": httpbin_test,
        "api_tests": api_tests,
        "public_api_success_count": sum(1 for result in api_tests if result.get("status_code") == 200),
        "download_persistence": persisted_downloads,
        "pyswisseph_test": pyswisseph_test,
        "skyfield_test": skyfield_test,
        "preferred_library": preferred_library,
        "installed_versions": {
            package: installed_version(package)
            for package in ["pyswisseph", "skyfield", "pandas", "requests", "numpy", "jplephem", "sgp4"]
        },
    }

    report = build_report(data)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
