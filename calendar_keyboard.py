from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import calendar

class CalendarKeyboard:
    def __init__(self):
        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def create_calendar(self, year=None, month=None):
        now = datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month

        keyboard = []
        
        # First row - Month and Year
        row = [
            InlineKeyboardButton(
                f"{self.months[month-1]} {year}",
                callback_data="ignore"
            )
        ]
        keyboard.append(row)
        
        # Second row - Days of week
        row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            row.append(InlineKeyboardButton(day, callback_data="ignore"))
        keyboard.append(row)

        # Calendar days
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(InlineKeyboardButton(" ", callback_data="ignore"))
                else:
                    # Format: YYYY-MM-DD
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    row.append(InlineKeyboardButton(
                        str(day),
                        callback_data=f"date_{date_str}"
                    ))
            keyboard.append(row)
        
        # Navigation buttons
        nav_row = []
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        nav_row.extend([
            InlineKeyboardButton(
                "<<",
                callback_data=f"prev_{prev_year}_{prev_month}"
            ),
            InlineKeyboardButton(
                ">>",
                callback_data=f"next_{next_year}_{next_month}"
            )
        ])
        keyboard.append(nav_row)

        return InlineKeyboardMarkup(keyboard)

    def process_calendar_selection(self, callback_query):
        data = callback_query.data
        if data.startswith("date_"):
            return data.split("_")[1]  # Returns YYYY-MM-DD
        elif data.startswith(("prev_", "next_")):
            _, year, month = data.split("_")
            return self.create_calendar(int(year), int(month))
        return None 