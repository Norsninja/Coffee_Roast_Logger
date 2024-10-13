import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Define file path for storing roast data
folder_path = 'roasting_data/'
os.makedirs(folder_path, exist_ok=True)

# Function to save roast data to CSV
def save_roast_data(roast_name, roast_date, start_weight, end_weight, first_crack_start, first_crack_end, cooling_start, data_entries):
    # Create the file path for the new roast
    file_name = f"{roast_name.replace(' ', '_').lower()}_{datetime.strptime(roast_date, '%m-%d-%y').strftime('%Y-%m-%d')}.csv"
    file_path = os.path.join(folder_path, file_name)

    # Prepare data to record
    headers = ['Minute', 'Bean Temperature (Bt)', 'Exhaust Temperature (Et)', 'Fan Power', 'Heat Setting']
    metadata = {
        'Roast Name': roast_name,
        'Roast Date': roast_date,
        'Starting Weight': start_weight,
        'Ending Weight': end_weight,
        'First Crack Start': first_crack_start,
        'First Crack End': first_crack_end,
        'Cooling Start': cooling_start
    }

    # Open CSV file for writing roast data
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write roast metadata as comments
        file.write(f'# {roast_name}\n')
        file.write(f'# Date: {roast_date}\n')
        file.write(f'# Start Weight: {start_weight}g\n')
        file.write(f'# End Weight: {end_weight}g\n')
        file.write(f'# First Crack Start: {first_crack_start}\n')
        file.write(f'# First Crack End: {first_crack_end}\n')
        file.write(f'# Cooling Start: {cooling_start}\n')

        # Write headers for data collection
        writer.writerow(headers)

        # Write row data to CSV
        for entry in data_entries:
            writer.writerow(entry)

    messagebox.showinfo('Success', f'Roast data saved to {file_path}')

# GUI for recording roast data
def record_roast_data_gui():
    # Create main window
    root = tk.Tk()
    root.title('Coffee Roast Data Recorder')
    root.geometry('900x650')
    style = ttk.Style(root)
    style.theme_use('clam')

    # Configure columns for even spacing
    for i in range(14):
        root.columnconfigure(i, weight=1)

    # Save roast data to file
    def save_data():
        # Gather metadata from form
        roast_name = roast_name_entry.get()
        roast_date = roast_date_entry.get().replace('/', '-')
        start_weight = start_weight_entry.get()
        end_weight = end_weight_entry.get()
        first_crack_start = first_crack_start_entry.get()
        first_crack_end = first_crack_end_entry.get()
        cooling_start = cooling_start_entry.get()

        if not roast_name or not roast_date or not start_weight or not end_weight or not first_crack_start or not first_crack_end or not cooling_start:
            messagebox.showerror('Error', 'Please fill in all fields.')
            return

        # Gather data entries from form
        data_entries = []
        for i in range(1, 13):
            bean_temp = bean_temp_entries[i - 1].get()
            exhaust_temp = exhaust_temp_entries[i - 1].get()
            fan_power = fan_power_entries[i - 1].get()
            heat_setting = heat_setting_entries[i - 1].get()

            if not bean_temp or not exhaust_temp:
                messagebox.showerror('Error', f'Missing data for minute {i}. Please fill in all fields.')
                return

            data_entries.append([i, float(bean_temp), float(exhaust_temp), fan_power, heat_setting])

        save_roast_data(
            roast_name,
            roast_date,
            float(start_weight),
            float(end_weight),
            first_crack_start,
            first_crack_end,
            cooling_start,
            data_entries
        )
        root.destroy()

    # UI Elements for Metadata Frame
    metadata_frame = ttk.LabelFrame(root, text='Enter Roast Metadata', padding=(10, 10))
    metadata_frame.grid(row=0, column=0, columnspan=14, padx=10, pady=10, sticky='ew')
    
    ttk.Label(metadata_frame, text='Roast Name:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    roast_name_entry = ttk.Entry(metadata_frame, width=30)
    roast_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='Roast Date:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    roast_date_entry = DateEntry(metadata_frame, width=28, background='darkblue', foreground='white', borderwidth=2)
    roast_date_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='Starting Weight (grams):').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    start_weight_entry = ttk.Entry(metadata_frame, width=30)
    start_weight_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='Ending Weight (grams):').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    end_weight_entry = ttk.Entry(metadata_frame, width=30)
    end_weight_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='First Crack Start (e.g., 8:10):').grid(row=4, column=0, sticky='e', padx=5, pady=5)
    first_crack_start_entry = ttk.Entry(metadata_frame, width=30)
    first_crack_start_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='First Crack End (e.g., 10:30):').grid(row=5, column=0, sticky='e', padx=5, pady=5)
    first_crack_end_entry = ttk.Entry(metadata_frame, width=30)
    first_crack_end_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(metadata_frame, text='Cooling Start (e.g., 12:00):').grid(row=6, column=0, sticky='e', padx=5, pady=5)
    cooling_start_entry = ttk.Entry(metadata_frame, width=30)
    cooling_start_entry.grid(row=6, column=1, padx=5, pady=5)

    # UI Elements for Data Entry Frame
    data_frame = ttk.LabelFrame(root, text='Enter Temperature Data (1-12 minutes)', padding=(10, 10))
    data_frame.grid(row=7, column=0, columnspan=14, padx=10, pady=10, sticky='ew')

    # Labels for columns
    ttk.Label(data_frame, text='Minute').grid(row=0, column=0)
    for i in range(1, 13):
        ttk.Label(data_frame, text=f'{i}').grid(row=0, column=i)

    ttk.Label(data_frame, text='Bean Temperature (Bt)').grid(row=1, column=0, sticky='e', padx=2, pady=2)
    bean_temp_entries = []
    for i in range(1, 13):
        bean_temp_entry = ttk.Entry(data_frame, width=10)
        bean_temp_entry.grid(row=1, column=i, padx=1, pady=2)
        bean_temp_entries.append(bean_temp_entry)

    ttk.Label(data_frame, text='Exhaust Temperature (Et)').grid(row=2, column=0, sticky='e', padx=2, pady=2)
    exhaust_temp_entries = []
    for i in range(1, 13):
        exhaust_temp_entry = ttk.Entry(data_frame, width=10)
        exhaust_temp_entry.grid(row=2, column=i, padx=1, pady=2)
        exhaust_temp_entries.append(exhaust_temp_entry)

    ttk.Label(data_frame, text='Fan Power (1-10)').grid(row=3, column=0, sticky='e', padx=2, pady=2)
    fan_power_entries = []
    for i in range(1, 13):
        fan_power_entry = ttk.Entry(data_frame, width=10)
        fan_power_entry.grid(row=3, column=i, padx=1, pady=2)
        fan_power_entries.append(fan_power_entry)

    ttk.Label(data_frame, text='Heat Setting (1-10)').grid(row=4, column=0, sticky='e', padx=2, pady=2)
    heat_setting_entries = []
    for i in range(1, 13):
        heat_setting_entry = ttk.Entry(data_frame, width=10)
        heat_setting_entry.grid(row=4, column=i, padx=1, pady=2)
        heat_setting_entries.append(heat_setting_entry)

    # Button to save data and exit
    save_button = ttk.Button(root, text='Save Roast Data', command=save_data)
    save_button.grid(row=15, column=0, columnspan=14, pady=20)

    # Run the Tkinter event loop
    root.mainloop()

# Run data recording function if this script is executed directly
if __name__ == '__main__':
    record_roast_data_gui()