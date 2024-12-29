# IQFeed Data Downloader

This project allows you to download historical data from IQFeed for specified symbols and save it as text files.

## Features
- Fetch historical interval data using the `HIT` command.
- Save data locally in organized files.
- Supports downloading data for multiple symbols in one run.

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/nketiah1717/iqdownloader.git
   ```
2. Navigate to the project directory:
   ```
   cd iqdownloader
   ```
3. Create and activate a virtual environment:
   - **Windows**:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
4. Install required dependencies (if any):
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Configure your symbols and date range in `iqfeed_data_loader.py`:
   - Update the `symbols`, `interval`, `start_date`, and `end_date` variables as needed.
2. Run the script:
   ```
   python iqfeed_data_loader.py
   ```
3. The data will be saved in the specified directory (default: `~/Desktop/history/etf`).

## Directory Structure
```
iqdownloader/
├── iqfeed_data_loader.py  # Main script
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── data/                  # Folder where downloaded data is saved
├── venv/                  # Virtual environment (not included in Git)
```

## License
This project is licensed under the MIT License.
