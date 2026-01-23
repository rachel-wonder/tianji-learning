"""
Lunar Calendar Template Generator
Generates the HTML/CSS/JS for the lunar calendar dropdown
"""

def generate_calendar_html(lunar_data, today_display, is_archive_page=False):
    """Generate the calendar HTML with lunar information."""

    # Build calendar grid
    calendar_html = ""
    for week in lunar_data['calendar']:
        calendar_html += '<div class="calendar-week">'
        for day_data in week:
            if day_data is None:
                calendar_html += '<div class="calendar-day empty"></div>'
            else:
                today_class = ' today' if day_data['is_today'] else ''

                # Determine if date is clickable (from Jan 21 to today)
                year = lunar_data['year']
                month = lunar_data['month']
                day = day_data['day']
                date_str = f"{year}-{month:02d}-{day:02d}"

                # Check if date is in valid range (Jan 21 to today)
                is_clickable = day_data.get('is_clickable', False)
                disabled_class = '' if is_clickable else ' disabled'

                # Build URL for navigation
                url_prefix = "" if is_archive_page else "archive/"
                onclick = f'onclick="navigateToDate(\'{url_prefix}{date_str}.html\')"' if is_clickable else ''

                calendar_html += f'''
                <div class="calendar-day{today_class}{disabled_class}" {onclick}>
                    <div class="solar-day">{day}</div>
                    <div class="lunar-day">{day_data['lunar_day']}</div>
                </div>'''
        calendar_html += '</div>'

    return calendar_html


def generate_calendar_css():
    """Generate CSS for the lunar calendar."""
    return '''
        .calendar-container {
            position: relative;
            display: inline-block;
            margin-bottom: 12px;
        }
        .calendar-button {
            padding: 4px 12px;
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 20px;
            color: white;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .calendar-button:hover {
            background: rgba(255,255,255,0.3);
        }
        .calendar-dropdown {
            display: none;
            position: absolute;
            top: 35px;
            left: 0;
            background: var(--color-surface);
            border: 2px solid var(--color-primary);
            border-radius: var(--radius-md);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            padding: 16px;
            z-index: 1000;
            min-width: 320px;
        }
        .calendar-dropdown.show {
            display: block;
        }
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--color-primary);
        }
        .month-nav-btn {
            background: none;
            border: none;
            color: var(--color-primary);
            font-size: 1.2rem;
            cursor: pointer;
            padding: 4px 8px;
            transition: all 0.2s ease;
        }
        .month-nav-btn:hover {
            background: var(--color-background);
            border-radius: 4px;
        }
        .calendar-weekdays {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            margin-bottom: 8px;
        }
        .calendar-weekday {
            text-align: center;
            font-size: 0.75rem;
            color: var(--color-text-light);
            padding: 4px;
        }
        .calendar-week {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            margin-bottom: 4px;
        }
        .calendar-day {
            text-align: center;
            padding: 8px 4px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .calendar-day:hover {
            background: var(--color-background);
        }
        .calendar-day.today {
            background: var(--color-primary);
            color: white;
        }
        .calendar-day.empty {
            cursor: default;
        }
        .calendar-day.disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        .calendar-day.disabled:hover {
            background: transparent;
        }
        .solar-day {
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--color-text);
        }
        .lunar-day {
            font-size: 0.7rem;
            color: var(--color-text-light);
            margin-top: 2px;
        }
        .calendar-day.today .solar-day {
            color: white;
        }
        .calendar-day.today .lunar-day {
            color: rgba(255,255,255,0.8);
        }
    '''


def generate_calendar_js(all_months_data, current_year, current_month, is_archive_page=False):
    """Generate JavaScript for calendar interaction with month navigation."""
    import json

    # Convert Python data to JSON for JavaScript
    months_json = json.dumps(all_months_data, ensure_ascii=False)

    # Calculate the index of the current month (0-based, so January = 0, February = 1, etc.)
    current_index = current_month - 1

    url_prefix = "" if is_archive_page else "archive/"

    return f'''
        // Store all months data (Jan 2026 to Dec 2026)
        const allMonthsData = {months_json};
        let currentMonthIndex = {current_index};
        const urlPrefix = "{url_prefix}";

        function toggleCalendar() {{
            const dropdown = document.getElementById('calendar-dropdown');
            dropdown.classList.toggle('show');
        }}

        function navigateToDate(url) {{
            window.location.href = url;
        }}

        function changeMonth(direction) {{
            currentMonthIndex += direction;

            // Boundary check (0 = January 2026, 11 = December 2026)
            if (currentMonthIndex < 0) {{
                currentMonthIndex = 0;
                return;
            }}
            if (currentMonthIndex >= allMonthsData.length) {{
                currentMonthIndex = allMonthsData.length - 1;
                return;
            }}

            renderCalendar(currentMonthIndex);
        }}

        function renderCalendar(monthIndex) {{
            const monthData = allMonthsData[monthIndex];
            const year = monthData.year;
            const month = monthData.month;

            // Update header
            document.getElementById('calendar-month-year').textContent = year + '年' + month + '月';

            // Generate calendar HTML
            let calendarHTML = '';
            const today = new Date();
            const todayYear = today.getFullYear();
            const todayMonth = today.getMonth() + 1;
            const todayDay = today.getDate();

            monthData.calendar.forEach(week => {{
                calendarHTML += '<div class="calendar-week">';
                week.forEach(dayData => {{
                    if (dayData === null) {{
                        calendarHTML += '<div class="calendar-day empty"></div>';
                    }} else {{
                        const isToday = (year === todayYear && month === todayMonth && dayData.day === todayDay);
                        const todayClass = isToday ? ' today' : '';
                        const disabledClass = dayData.is_clickable ? '' : ' disabled';

                        const dateStr = year + '-' + String(month).padStart(2, '0') + '-' + String(dayData.day).padStart(2, '0');
                        const onclick = dayData.is_clickable ?
                            'onclick="navigateToDate(\\'' + urlPrefix + dateStr + '.html\\')"' : '';

                        calendarHTML += '<div class="calendar-day' + todayClass + disabledClass + '" ' + onclick + '>';
                        calendarHTML += '<div class="solar-day">' + dayData.day + '</div>';
                        calendarHTML += '<div class="lunar-day">' + dayData.lunar_day + '</div>';
                        calendarHTML += '</div>';
                    }}
                }});
                calendarHTML += '</div>';
            }});

            // Update calendar grid
            const calendarContainer = document.querySelector('.calendar-dropdown');
            const weekdaysDiv = calendarContainer.querySelector('.calendar-weekdays');

            // Remove old calendar weeks
            const oldWeeks = calendarContainer.querySelectorAll('.calendar-week');
            oldWeeks.forEach(week => week.remove());

            // Insert new calendar after weekdays
            weekdaysDiv.insertAdjacentHTML('afterend', calendarHTML);
        }}

        // Close calendar when clicking outside
        document.addEventListener('click', function(event) {{
            const container = document.querySelector('.calendar-container');
            if (container && !container.contains(event.target)) {{
                const dropdown = document.getElementById('calendar-dropdown');
                if (dropdown) {{
                    dropdown.classList.remove('show');
                }}
            }}
        }});
    '''
