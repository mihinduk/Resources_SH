# LTS Data Management

This repository tracks data stored on Long Term Storage (LTS) systems. The data is now maintained in CSV format for better version control and collaboration.

## Files

- `lts_data1.csv` - Data stored in `/lts/sahlab/data1/DATA_DOWNLOADS`
- `lts_data3.csv` - Data stored in `/lts/sahlab/data3/DATA_DOWNLOADS_2`
- `lts_data4.csv` - Data stored in `/lts/sahlab/data4/DATA_DOWNLOADS_3`
- `lts_rc2.csv` - RC2 virome data

## Using the LTS Manager Script

The `lts_manager.py` script provides an easy way to manage the data:

### List all entries
```bash
python3 lts_manager.py list
```

### List entries from specific storage
```bash
python3 lts_manager.py list -s data1
```

### Search for a project
```bash
python3 lts_manager.py list -p "virome"
```

### Add a new entry
```bash
python3 lts_manager.py add data1 "NewProject2024" "Kathie's Mouse Study" -n "500 samples, sequenced on NextSeq"
```

### Update notes for an existing entry
```bash
python3 lts_manager.py update data1 "NewProject2024" "Kathie's Mouse Study" "500 samples, sequenced on NextSeq, analysis complete"
```

### Search across all files
```bash
python3 lts_manager.py search "mouse"
```

### Export back to Excel
```bash
python3 lts_manager.py export
```

## Manual Editing

You can also edit the CSV files directly:
1. Open in Excel or any text editor
2. Add new rows following the format: Directory,Project,Notes
3. Save the file
4. Commit and push changes

## Workflow for Updates

1. Pull latest changes: `git pull`
2. Add/update data using the script or manual editing
3. Commit changes: `git add . && git commit -m "Add new project data"`
4. Push to GitHub: `git push`

## Original Excel File

The original Excel file `2020_11_10_stored_on_lts_KM.xlsx` is preserved in the repository for reference.