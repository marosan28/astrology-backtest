# Capability Report

Generated at: 2026-07-15T15:34:20.973792+00:00

## Assumptions

- All network checks are single unauthenticated GET requests made at runtime.
- The timestamp under test is 2026-07-15 12:00:00 UTC.
- Longitudes are reported in degrees from 0° to 360°.
- pyswisseph tropical calculations use swe.calc_ut with FLG_SWIEPH | FLG_SPEED, and sidereal calculations add FLG_SIDEREAL after calling swe.set_sid_mode.
- Skyfield, if successful, uses geocentric apparent ecliptic longitude of date from de421.bsp obtained through Skyfield's loader.

## Step 1 — Execution Environment

- OS: Linux-6.17.0-1018-azure-x86_64-with-glibc2.39
- Python: 3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0]
- Shell command success: True
- pip install command success: True
- File create/modify success: True / True
- Python script execution success: True
- Outbound HTTPS success (httpbin): False
- Public API query success count: 0 / 4
- Downloaded dataset persistence check: not tested; no successful downloads

### Shell Test

```json
{
  "command": "printf shell_command_ok",
  "success": true,
  "returncode": 0,
  "stdout": "shell_command_ok",
  "stderr": ""
}
```

### pip Test

```json
{
  "command": "/usr/bin/python -m pip install --disable-pip-version-check --quiet --no-deps requests==2.34.2",
  "success": true,
  "returncode": 0,
  "stdout": "",
  "stderr": ""
}
```

### File and Python Execution Tests

```json
{
  "file_test": {
    "path": "/home/runner/work/astrology-backtest/astrology-backtest/environment/file_write_probe.txt",
    "created": true,
    "modified": true,
    "exists_after_write": true,
    "size_bytes": 55,
    "final_contents": "created=2026-07-15T15:34:20.748936+00:00\nmodified=true"
  },
  "python_exec_test": {
    "command": "/usr/bin/python /home/runner/work/astrology-backtest/astrology-backtest/environment/python_exec_probe.py",
    "success": true,
    "returncode": 0,
    "stdout": "python_probe_ok",
    "stderr": "",
    "probe_script": "/home/runner/work/astrology-backtest/astrology-backtest/environment/python_exec_probe.py"
  }
}
```

## Step 2 — Astronomical Libraries

### Preferred Library for 1800–2030

- Selected library: pyswisseph
- Why: Preferred for 1800–2030 because it successfully computed positions locally in this environment, supports built-in sidereal modes such as Lahiri and Fagan–Bradley, and avoids Skyfield's need to choose and fetch a separate JPL ephemeris file. In this run the requested Swiss ephemeris file mode fell back to the built-in Moshier ephemeris because Swiss data files were not installed, so final production calculations should pin manually sourced Swiss ephemeris files for maximum reproducibility.

### pyswisseph

```json
{
  "library": "pyswisseph",
  "target_datetime_utc": "2026-07-15T12:00:00+00:00",
  "imported": true,
  "version": "2.10.3.2",
  "calculation_settings": "swe.calc_ut(julian_day, planet, FLG_SWIEPH | FLG_SPEED) for tropical positions; geocentric ecliptic longitude in the default tropical zodiac.",
  "julian_day_ut": 2461237.0,
  "tropical_positions": {
    "Saturn": {
      "longitude_deg": 14.64085241035637,
      "latitude_deg": -2.4490862980779147,
      "distance_au": 9.256458571589336,
      "speed_longitude_deg_per_day": 0.019297122322536477,
      "returned_flags": 260,
      "ephemeris_source": "Moshier fallback"
    },
    "Neptune": {
      "longitude_deg": 4.400803279161819,
      "latitude_deg": -1.3790576345771461,
      "distance_au": 29.53970472608296,
      "speed_longitude_deg_per_day": -0.004311261787431687,
      "returned_flags": 260,
      "ephemeris_source": "Moshier fallback"
    }
  },
  "sidereal_positions": {
    "Lahiri": {
      "application": "Applied SIDM_LAHIRI by calling swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0) and then swe.calc_ut(..., FLG_SWIEPH | FLG_SPEED | FLG_SIDEREAL).",
      "positions": {
        "Saturn": {
          "longitude_deg": 350.41051810937734,
          "latitude_deg": -2.4490862980779142,
          "distance_au": 9.256458571589336,
          "speed_longitude_deg_per_day": 0.01923415397594968,
          "returned_flags": 65860,
          "ephemeris_source": "Moshier fallback"
        },
        "Neptune": {
          "longitude_deg": 340.1704689781828,
          "latitude_deg": -1.379057634577146,
          "distance_au": 29.53970472608296,
          "speed_longitude_deg_per_day": -0.004373881375675947,
          "returned_flags": 65860,
          "ephemeris_source": "Moshier fallback"
        }
      }
    },
    "Fagan-Bradley": {
      "application": "Applied SIDM_FAGAN_BRADLEY by calling swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY, 0, 0) and then swe.calc_ut(..., FLG_SWIEPH | FLG_SPEED | FLG_SIDEREAL).",
      "positions": {
        "Saturn": {
          "longitude_deg": 349.52731046509274,
          "latitude_deg": -2.4490862980779142,
          "distance_au": 9.256458571589336,
          "speed_longitude_deg_per_day": 0.019234153975949683,
          "returned_flags": 65860,
          "ephemeris_source": "Moshier fallback"
        },
        "Neptune": {
          "longitude_deg": 339.2872613338982,
          "latitude_deg": -1.379057634577146,
          "distance_au": 29.53970472608296,
          "speed_longitude_deg_per_day": -0.004373881375675944,
          "returned_flags": 65860,
          "ephemeris_source": "Moshier fallback"
        }
      }
    }
  },
  "ephemeris_management": {
    "bundled_files_detected": false,
    "auto_download_behavior": "No auto-download observed.",
    "manual_sourcing_required_for_swiss_files": true,
    "observed_runtime_source": "Moshier fallback"
  }
}
```

### skyfield

```json
{
  "library": "skyfield",
  "target_datetime_utc": "2026-07-15T12:00:00+00:00",
  "imported": true,
  "version": "1.54",
  "calculation_settings": "Skyfield geocentric apparent positions with ecliptic_latlon(epoch='date'); auto-download attempt for de421.bsp via Loader.",
  "ephemeris_management": {
    "bundled_files_detected": false,
    "auto_download_behavior": "Attempts to download de421.bsp into the local Skyfield cache.",
    "manual_sourcing_may_be_needed": true
  },
  "error": "Traceback (most recent call last):\n  File \"/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py\", line 253, in test_skyfield\n    planets = loader(\"de421.bsp\")\n              ^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/.local/lib/python3.12/site-packages/skyfield/iokit.py\", line 193, in __call__\n    path = self._assure(url, filename, reload, backup)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/.local/lib/python3.12/site-packages/skyfield/iokit.py\", line 214, in _assure\n    download(url, path, self.verbose, backup=backup)\n  File \"/home/runner/.local/lib/python3.12/site-packages/skyfield/iokit.py\", line 494, in download\n    raise e2\nOSError: cannot download https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp because <urlopen error [Errno -5] No address associated with hostname>"
}
```

## Step 3 — Sidereal Calculations

Sidereal positions were computed with pyswisseph using library-managed sidereal mode switching; no manual subtraction was used.

```json
{
  "Lahiri": {
    "application": "Applied SIDM_LAHIRI by calling swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0) and then swe.calc_ut(..., FLG_SWIEPH | FLG_SPEED | FLG_SIDEREAL).",
    "positions": {
      "Saturn": {
        "longitude_deg": 350.41051810937734,
        "latitude_deg": -2.4490862980779142,
        "distance_au": 9.256458571589336,
        "speed_longitude_deg_per_day": 0.01923415397594968,
        "returned_flags": 65860,
        "ephemeris_source": "Moshier fallback"
      },
      "Neptune": {
        "longitude_deg": 340.1704689781828,
        "latitude_deg": -1.379057634577146,
        "distance_au": 29.53970472608296,
        "speed_longitude_deg_per_day": -0.004373881375675947,
        "returned_flags": 65860,
        "ephemeris_source": "Moshier fallback"
      }
    }
  },
  "Fagan-Bradley": {
    "application": "Applied SIDM_FAGAN_BRADLEY by calling swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY, 0, 0) and then swe.calc_ut(..., FLG_SWIEPH | FLG_SPEED | FLG_SIDEREAL).",
    "positions": {
      "Saturn": {
        "longitude_deg": 349.52731046509274,
        "latitude_deg": -2.4490862980779142,
        "distance_au": 9.256458571589336,
        "speed_longitude_deg_per_day": 0.019234153975949683,
        "returned_flags": 65860,
        "ephemeris_source": "Moshier fallback"
      },
      "Neptune": {
        "longitude_deg": 339.2872613338982,
        "latitude_deg": -1.379057634577146,
        "distance_au": 29.53970472608296,
        "speed_longitude_deg_per_day": -0.004373881375675944,
        "returned_flags": 65860,
        "ephemeris_source": "Moshier fallback"
      }
    }
  }
}
```

## Step 4 — Historical Research API Access

### HTTPBin

- URL: https://httpbin.org/get
- Status: None
- Data returned: False
- Auth required: unknown
- Saved locally: False

```text
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 203, in _new_conn
    sock = connection.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 963, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -5] No address associated with hostname

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 492, in _make_request
    raise new_e
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 468, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1109, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 611, in connect
    self.sock = sock = self._new_conn()
                       ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 210, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x7fa9605f13d0>: Failed to resolve 'httpbin.org' ([Errno -5] No address associated with hostname)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 696, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 845, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 517, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='httpbin.org', port=443): Max retries exceeded with url: /get (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f13d0>: Failed to resolve 'httpbin.org' ([Errno -5] No address associated with hostname)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py", line 119, in fetch_endpoint
    response = requests.get(
               ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 87, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 71, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 729, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='httpbin.org', port=443): Max retries exceeded with url: /get (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f13d0>: Failed to resolve 'httpbin.org' ([Errno -5] No address associated with hostname)"))
```

### Crossref

- URL: https://api.crossref.org/works?query=Saturn+Neptune+conjunction+history&rows=3
- Status: None
- Data returned: False
- Auth required: unknown
- Saved locally: False

```text
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 203, in _new_conn
    sock = connection.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 963, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -5] No address associated with hostname

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 492, in _make_request
    raise new_e
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 468, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1109, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 611, in connect
    self.sock = sock = self._new_conn()
                       ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 210, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x7fa9605f21b0>: Failed to resolve 'api.crossref.org' ([Errno -5] No address associated with hostname)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 696, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 845, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 517, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.crossref.org', port=443): Max retries exceeded with url: /works?query=Saturn+Neptune+conjunction+history&rows=3 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f21b0>: Failed to resolve 'api.crossref.org' ([Errno -5] No address associated with hostname)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py", line 119, in fetch_endpoint
    response = requests.get(
               ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 87, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 71, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 729, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.crossref.org', port=443): Max retries exceeded with url: /works?query=Saturn+Neptune+conjunction+history&rows=3 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f21b0>: Failed to resolve 'api.crossref.org' ([Errno -5] No address associated with hostname)"))
```

### OpenAlex

- URL: https://api.openalex.org/works?search=Uranus+Pluto+conjunction+history&per_page=3
- Status: None
- Data returned: False
- Auth required: unknown
- Saved locally: False

```text
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 203, in _new_conn
    sock = connection.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 963, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -5] No address associated with hostname

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 492, in _make_request
    raise new_e
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 468, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1109, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 611, in connect
    self.sock = sock = self._new_conn()
                       ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 210, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x7fa9605f13a0>: Failed to resolve 'api.openalex.org' ([Errno -5] No address associated with hostname)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 696, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 845, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 517, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.openalex.org', port=443): Max retries exceeded with url: /works?search=Uranus+Pluto+conjunction+history&per_page=3 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f13a0>: Failed to resolve 'api.openalex.org' ([Errno -5] No address associated with hostname)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py", line 119, in fetch_endpoint
    response = requests.get(
               ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 87, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 71, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 729, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.openalex.org', port=443): Max retries exceeded with url: /works?search=Uranus+Pluto+conjunction+history&per_page=3 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f13a0>: Failed to resolve 'api.openalex.org' ([Errno -5] No address associated with hostname)"))
```

### Wikidata

- URL: https://www.wikidata.org/w/api.php?action=wbsearchentities&search=French+Revolution&language=en&format=json
- Status: None
- Data returned: False
- Auth required: unknown
- Saved locally: False

```text
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 203, in _new_conn
    sock = connection.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 963, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -5] No address associated with hostname

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 492, in _make_request
    raise new_e
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 468, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1109, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 611, in connect
    self.sock = sock = self._new_conn()
                       ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 210, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x7fa9605f2990>: Failed to resolve 'www.wikidata.org' ([Errno -5] No address associated with hostname)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 696, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 845, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 517, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.wikidata.org', port=443): Max retries exceeded with url: /w/api.php?action=wbsearchentities&search=French+Revolution&language=en&format=json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f2990>: Failed to resolve 'www.wikidata.org' ([Errno -5] No address associated with hostname)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py", line 119, in fetch_endpoint
    response = requests.get(
               ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 87, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 71, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 729, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.wikidata.org', port=443): Max retries exceeded with url: /w/api.php?action=wbsearchentities&search=French+Revolution&language=en&format=json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f2990>: Failed to resolve 'www.wikidata.org' ([Errno -5] No address associated with hostname)"))
```

### World Bank

- URL: https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=1900:1910&format=json&per_page=5
- Status: None
- Data returned: False
- Auth required: unknown
- Saved locally: False

```text
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 203, in _new_conn
    sock = connection.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 963, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -5] No address associated with hostname

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 791, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 492, in _make_request
    raise new_e
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 468, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1109, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 611, in connect
    self.sock = sock = self._new_conn()
                       ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 210, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x7fa9605f30b0>: Failed to resolve 'api.worldbank.org' ([Errno -5] No address associated with hostname)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 696, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 845, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 517, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.worldbank.org', port=443): Max retries exceeded with url: /v2/country/all/indicator/NY.GDP.MKTP.CD?date=1900:1910&format=json&per_page=5 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f30b0>: Failed to resolve 'api.worldbank.org' ([Errno -5] No address associated with hostname)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/astrology-backtest/astrology-backtest/scripts/capability_test.py", line 119, in fetch_endpoint
    response = requests.get(
               ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 87, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/api.py", line 71, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/requests/adapters.py", line 729, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.worldbank.org', port=443): Max retries exceeded with url: /v2/country/all/indicator/NY.GDP.MKTP.CD?date=1900:1910&format=json&per_page=5 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fa9605f30b0>: Failed to resolve 'api.worldbank.org' ([Errno -5] No address associated with hostname)"))
```

## Installed Package Versions

```json
{
  "pyswisseph": "2.10.3.2",
  "skyfield": "1.54",
  "pandas": "3.0.3",
  "requests": "2.34.2",
  "numpy": "2.5.1",
  "jplephem": "2.24",
  "sgp4": "2.27"
}
```
