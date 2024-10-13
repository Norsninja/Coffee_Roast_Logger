# Coffee_Roast_Logger

**Record your coffee roast measurements then visualize them. For post roast note logging.**

## Images

![Roast Dashboard](roast_dashboard.png)

![Roast Recorder](roast_recorder.png)

## Introduction

Welcome to Coffee_Roast_Logger! This is a tool designed to help you record, log, and visualize your coffee roasting measurements. As a coffee roasting enthusiast, I'm learning more about roasting every day, and I'm excited to share these resources to help improve the roasting process.

## Getting Started

### 1. Manual Note-Taking

To get started, you can use the **PDF roasting log** for manual note-taking. Simply download and print the PDF to log your roasting measurements as you go.

If you prefer a printed journal, I've created the **Roast Master's Journal** by Derry Luwak Publishing, available on Amazon. This journal is designed to help you keep detailed and consistent records of your roasts in a professional notebook.

### 2. Recording Roasts Digitally

Once you've manually recorded your roasts, you can enter the data into the **Coffee Roast Data Recorder** Python script to create a digital record of each roast. This script saves each roast's data in a CSV file, allowing you to store and organize your roasting history easily.

### 3. Setting Up the Environment

- **Create a Folder**: Create a folder named `roasting_data` in the root directory of the project. The data recorder script will save individual CSV files for each roast into this folder.
- **Record Your Data**: Use the `coffee_roast_data_recorder.py` script to enter your roast data from your notes. Each roast is saved as a CSV file in the `roasting_data` folder.

### 4. Visualizing Your Roasts

After you've logged your roast data, you can visualize it using the **Coffee Roast Dashboard** by running the `coffee_roast_dash_imp.py` file. The dashboard will provide:

- **Temperature Over Time**: Visualize how the bean and exhaust temperatures change over the duration of the roast.
- **Rate of Rise (RoR)**: Analyze the rate of temperature change, which is crucial for understanding how the roast is developing at each stage.

This dashboard provides a simple and accessible way to visualize your roasting process, similar to more well-known roasting programs but with less complexity, making it perfect for beginners and intermediate roasters.

## Requirements

To run Coffee_Roast_Logger, you will need:

- Python 3.x
- Dash (`pip install dash`)
- Plotly (`pip install plotly`)
- Pandas (`pip install pandas`)

Make sure you have these dependencies installed before attempting to run the scripts.

## Usage

1. **Manual Logging**: Use the provided PDF to manually log your roast.
2. **Data Entry**: Run `coffee_roast_data_recorder.py` to input your recorded data.
3. **Visualization**: Run `coffee_roast_dash_imp.py` to visualize the roast.

## Features

- **Post-Roast Data Logging**: Input roast data after completion to keep detailed records.
- **Visualization Dashboard**: See trends in temperature and rate of rise with intuitive graphs.
- **CSV Storage**: All roasts are stored as individual CSV files for easy reference and analysis.

## Contributions

If you have any suggestions or would like to contribute, feel free to submit an issue or a pull request. I'm happy to collaborate with other coffee enthusiasts to keep improving the tools!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Thank you to the coffee roasting community for inspiring me to keep improving the tools available to roasters of all levels. Let's roast better together!

## Contact

For questions or comments, feel free to reach out. I'm always happy to discuss roasting, software, and anything coffee-related!
