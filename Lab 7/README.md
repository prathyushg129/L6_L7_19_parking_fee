# Lab 7 · Fuzz testing the parking fee application

Prathyush Gowda HP · PES1UG24AM201 · Class 5-D

| Deliverable | Contents |
| --- | --- |
| [Screenshot report](PES1UG24AM201_Lab7_Report.pdf) | Four PowerShell captures showing the application and test suite before and after the fix |
| [Parking fee application](parking_fee.py) | Validates same-day parking intervals, vehicle types and registration plates |
| [Hypothesis tests](test_parking_fee.py) | Seven tests covering arbitrary input, boundary values, standard rates and plate formatting |

## Run in PowerShell

From a folder where you want a fresh clone, run the following with Git and Python installed.

```powershell
git clone https://github.com/prathyushg129/L6_L7_19_parking_fee.git
Set-Location '.\L6_L7_19_parking_fee\Lab 7'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install hypothesis pytest
.\.venv\Scripts\python.exe parking_fee.py
.\.venv\Scripts\python.exe -m pytest -q --hypothesis-seed=201 test_parking_fee.py
```

For the example in the report, enter `09:30-11:45`, `bus` and `ka01ab1234` at the prompts. The time interval gives 135 minutes. The application explains the unsupported vehicle and continues to format the plate as `KA 01 AB 1234`.

## Test results

| Application version | Passed | Failed |
| --- | ---: | ---: |
| Starter application with completed tests | 1 | 6 |
| Fixed application with the same tests | 7 | 0 |
