# TimeTracker

A desktop application built with Python and Tkinter for tracking work hours and managing time balances. TimeTracker helps you monitor your daily work schedule, lunch breaks, and automatically calculates your time balance on a daily, weekly, and monthly basis.

## Features

- **Daily Time Tracking**
  - Record arrival time, lunch breaks, and departure time
  - Automatic daily balance calculation
  - Support for holidays and weekends

- **Balance Summaries**
  - Daily balance overview
  - Weekly balance (Sunday through Thursday)
  - Monthly balance with automatic calculations
  - 7.5-hour workday calculation

- **Calendar Integration**
  - Visual calendar interface for date selection
  - Weekend highlighting (Friday-Saturday)
  - Holiday management

- **Data Persistence**
  - Local SQLite database storage
  - Automatic data directory creation
  - Holiday tracking and management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/moxer-mmh/PPT.git
cd PPT
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Dependencies

- Python 3.x
- tkinter
- tkcalendar
- sqlite3 (included in Python standard library)

## Usage

1. Run the application:
```bash
python -m main.py
```

2. The main window will open with:
   - A calendar for date selection
   - Time entry fields for:
     - Arrival time
     - Lunch start
     - Lunch end
     - Departure time
   - Balance summary showing daily, weekly, and monthly totals

3. Enter times in 24-hour format (HH:MM)

4. Click "Save Entry" to store your time entry

## Work Schedule

- Work week: Sunday through Thursday
- Weekend: Friday and Saturday
- Working hours are tracked and calculated accordingly
- Holidays can be marked and are excluded from calculations

## Data Storage

TimeTracker stores all data locally in a SQLite database located at:
- Windows: `%LOCALAPPDATA%\TimeTracker\data\timetracker.db`
- Unix/MacOS: `~/TimeTracker/data/timetracker.db`

## Project Structure

```
PPT/
│
├── main.py
├── views/
│   ├── daily_view.py
│   ├── holidays_view.py
│   └── reports_view.py
│
├── controllers/
│   ├── daily_controller.py
│   ├── holidays_controller.py
│   └── reports_controller.py
│
├── models/
│   ├── time_entry.py
│   ├── holiday.py
│   └── database.py
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
└── requirements.txt

```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Requirements

Create a `requirements.txt` file with the following content:

```
tkcalendar==1.6.1
```

Note: Other dependencies are part of the Python standard library.

## Acknowledgments

- Icons and visual elements from Tkinter
- Calendar widget from tkcalendar

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.