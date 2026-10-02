# GitHub Actions Education Result Checker

This version modifies the interactive Python result checker so it can run from GitHub Actions.

## Files

- `result_action.py` - GitHub Actions compatible Python script
- `.github/workflows/result.yml` - workflow with manual inputs

## How to use

1. Upload these files to a GitHub repository.
2. Open the repository.
3. Go to **Actions**.
4. Select **Check Education Result**.
5. Click **Run workflow**.
6. Enter exam, year, roll/reg, and board number.
7. Run it.
8. Open the workflow run and see the Python output.

## Board numbers

1 Dhaka
2 Rajshahi
3 Chittogram
4 Jashore
5 Cumilla
6 Barishal
7 Sylhet
8 Dinajpur
9 Madrasah
10 Mymensingh
11 Technical
12 BOU

Note: The script uses the same Rajshahi Board API endpoint from the original code. GitHub Actions/network or the upstream API may reject the request, so successful execution depends on that endpoint being reachable.
