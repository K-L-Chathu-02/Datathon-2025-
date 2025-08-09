#!/usr/bin/env python3
"""
Combine all dataset CSV files into a single master CSV file
"""

import csv
import os

def read_csv_file(filename, main_col_name, sub_col_name):
    """Read CSV file and standardize column names"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle different column name variations
                main_category = row.get(main_col_name, '').strip()
                sub_category = row.get(sub_col_name, '').strip()
                image_file = row.get('image_file', '').strip()
                
                if image_file and main_category and sub_category:
                    data.append({
                        'image_file': image_file,
                        'main_category': main_category,
                        'sub_category': sub_category,
                        'dataset': os.path.splitext(filename)[0]  # Add dataset source
                    })
        print(f"✅ Loaded {len(data)} records from {filename}")
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
    
    return data

def main():
    # Define the CSV files and their column names
    csv_files = [
        ('graffitti_labels.csv', 'main_categories', 'sub_categories'),
        ('trash_labels.csv', 'main_category', 'sub_category'),
        ('potholes_labels.csv', 'main_categories', 'sub_categories'),
        ('damagedsigns_labeled_data.csv', 'main_category', 'sub_category')
    ]
    
    all_data = []
    
    print("🔄 Combining CSV files...")
    print()
    
    # Read all CSV files
    for filename, main_col, sub_col in csv_files:
        if os.path.exists(filename):
            file_data = read_csv_file(filename, main_col, sub_col)
            all_data.extend(file_data)
        else:
            print(f"⚠️  File not found: {filename}")
    
    print()
    print(f"📊 Total records collected: {len(all_data)}")
    
    # Write combined CSV
    if all_data:
        output_filename = 'combined_dataset_labels.csv'
        
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['image_file', 'main_category', 'sub_category', 'dataset']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"✅ Successfully created: {output_filename}")
        
        # Print summary statistics
        print()
        print("📈 Dataset Summary:")
        
        # Count by dataset
        dataset_counts = {}
        category_counts = {}
        subcategory_counts = {}
        
        for row in all_data:
            dataset = row['dataset']
            main_cat = row['main_category']
            sub_cat = row['sub_category']
            
            dataset_counts[dataset] = dataset_counts.get(dataset, 0) + 1
            category_counts[main_cat] = category_counts.get(main_cat, 0) + 1
            subcategory_counts[sub_cat] = subcategory_counts.get(sub_cat, 0) + 1
        
        print("\nBy Dataset:")
        for dataset, count in sorted(dataset_counts.items()):
            print(f"  {dataset}: {count} images")
        
        print("\nBy Main Category:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} images")
        
        print("\nBy Sub Category:")
        for subcategory, count in sorted(subcategory_counts.items()):
            print(f"  {subcategory}: {count} images")
        
        print(f"\n🎯 Ready for ML training with {len(all_data)} labeled images!")
    
    else:
        print("❌ No data to combine!")

if __name__ == "__main__":
    main()



