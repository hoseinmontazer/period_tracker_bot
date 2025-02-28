from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import calendar
import logging

logger = logging.getLogger(__name__)

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
        
        # Calculate previous month and year
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        
        # Calculate next month and year
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
        print("\n=== Calendar Keyboard Processing Selection ===")
        try:
            data = callback_query.data
            print(f"Processing callback data: {data}")
            
            if data == "ignore":
                print("Ignore button pressed")
                return None
                
            elif data.startswith(("prev_", "next_")):
                print(f"Navigation button pressed: {data}")
                _, year, month = data.split("_")
                year, month = int(year), int(month)
                print(f"Creating new calendar for {year}-{month}")
                new_markup = self.create_calendar(year, month)
                print("New calendar markup created")
                return None, new_markup
                
            elif data.startswith("date_"):
                print(f"Date selection detected: {data}")
                selected_date = data.split("_")[1]
                print(f"Returning selected date: {selected_date}")
                return selected_date
                
        except Exception as e:
            print(f"ERROR in calendar keyboard processing: {e}")
            logger.error("Calendar processing error", exc_info=True)
            return None
            
        print("No matching callback data pattern found")
        return None 