#!/usr/bin/env python3
"""
LTS Data Manager - Tool for managing Long Term Storage data tracking
"""

import pandas as pd
import argparse
import os
from datetime import datetime

# File mappings
FILE_MAPPING = {
    'data1': 'lts_data1.csv',
    'data3': 'lts_data3.csv',
    'data4': 'lts_data4.csv',
    'rc2': 'lts_rc2.csv'
}

def list_entries(storage=None, project=None):
    """List entries from CSV files with optional filtering"""
    results = []
    
    for storage_name, filename in FILE_MAPPING.items():
        if storage and storage != storage_name:
            continue
            
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            
            if project:
                # Case-insensitive search in Project column
                df = df[df['Project'].str.contains(project, case=False, na=False)]
            
            if not df.empty:
                print(f"\n=== {storage_name.upper()} ({filename}) ===")
                print(df.to_string(index=True))
                results.append((storage_name, df))
    
    return results

def add_entry(storage, directory, project, notes=None):
    """Add a new entry to the specified storage CSV"""
    if storage not in FILE_MAPPING:
        print(f"Error: Unknown storage '{storage}'. Choose from: {', '.join(FILE_MAPPING.keys())}")
        return False
    
    filename = FILE_MAPPING[storage]
    
    # Read existing data or create new DataFrame
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['Directory', 'Project', 'Notes'])
    
    # Check for duplicate
    if ((df['Directory'] == directory) & (df['Project'] == project)).any():
        print(f"Warning: Entry already exists for {directory}/{project}")
        response = input("Add anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Add new entry
    new_entry = pd.DataFrame([{
        'Directory': directory,
        'Project': project,
        'Notes': notes if notes else ''
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    
    # Save back to CSV
    df.to_csv(filename, index=False)
    print(f"Added entry to {filename}")
    return True

def update_notes(storage, directory, project, notes):
    """Update notes for an existing entry"""
    if storage not in FILE_MAPPING:
        print(f"Error: Unknown storage '{storage}'. Choose from: {', '.join(FILE_MAPPING.keys())}")
        return False
    
    filename = FILE_MAPPING[storage]
    
    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist")
        return False
    
    df = pd.read_csv(filename)
    
    # Find matching entry
    mask = (df['Directory'] == directory) & (df['Project'] == project)
    
    if not mask.any():
        print(f"Error: No entry found for {directory}/{project}")
        return False
    
    # Update notes
    df.loc[mask, 'Notes'] = notes
    
    # Save back to CSV
    df.to_csv(filename, index=False)
    print(f"Updated notes in {filename}")
    return True

def search_all(search_term):
    """Search across all CSV files for a term"""
    print(f"Searching for '{search_term}' across all files...")
    found = False
    
    for storage_name, filename in FILE_MAPPING.items():
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            
            # Search in all columns
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
            matches = df[mask]
            
            if not matches.empty:
                found = True
                print(f"\n=== Found in {storage_name.upper()} ({filename}) ===")
                print(matches.to_string(index=True))
    
    if not found:
        print("No matches found.")

def export_to_excel():
    """Export all CSV files back to Excel format"""
    output_file = f"lts_data_export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for storage_name, filename in FILE_MAPPING.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                df.to_excel(writer, sheet_name=storage_name, index=False)
                print(f"Exported {filename} to sheet '{storage_name}'")
    
    print(f"\nCreated Excel file: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Manage LTS data tracking')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List entries')
    list_parser.add_argument('-s', '--storage', help='Filter by storage (data1, data3, data4, rc2)')
    list_parser.add_argument('-p', '--project', help='Filter by project name (partial match)')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add new entry')
    add_parser.add_argument('storage', choices=FILE_MAPPING.keys(), help='Storage location')
    add_parser.add_argument('directory', help='Directory name')
    add_parser.add_argument('project', help='Project name')
    add_parser.add_argument('-n', '--notes', help='Optional notes')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update notes for existing entry')
    update_parser.add_argument('storage', choices=FILE_MAPPING.keys(), help='Storage location')
    update_parser.add_argument('directory', help='Directory name')
    update_parser.add_argument('project', help='Project name')
    update_parser.add_argument('notes', help='New notes')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search all files')
    search_parser.add_argument('term', help='Search term')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export all CSV files to Excel')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_entries(args.storage, args.project)
    elif args.command == 'add':
        add_entry(args.storage, args.directory, args.project, args.notes)
    elif args.command == 'update':
        update_notes(args.storage, args.directory, args.project, args.notes)
    elif args.command == 'search':
        search_all(args.term)
    elif args.command == 'export':
        export_to_excel()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()