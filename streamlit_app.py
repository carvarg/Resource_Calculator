import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

def estimate_headcount(start_date, total_hours, hours_per_shift=10, shifts_per_day=2, work_days_per_week=6, productivity_factor=1.0, ramp_up=10, peak_duration=20, ramp_down=10, view='Hours'):
    # Calculate the total working days based on work schedule
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    work_days = []
    current_date = start
    while len(work_days) < ramp_up + peak_duration + ramp_down:
        if work_days_per_week == 7 or current_date.weekday() != 6:  # Skip Sundays if work_days_per_week < 7
            work_days.append(current_date)
        current_date += timedelta(days=1)
    
    duration = len(work_days)
    elapsed_days = (work_days[-1] - start).days + 1
    
    # Generate day indices
    days = np.arange(duration)
    
    # Define piecewise work distribution (trapezoidal shape)
    work_distribution = np.zeros(duration)
    
    # Ramp-up phase (linear increase)
    for i in range(ramp_up):
        work_distribution[i] = (i + 1) / ramp_up
    
    # Peak phase (constant workload)
    work_distribution[ramp_up:ramp_up + peak_duration] = 1
    
    # Ramp-down phase (linear decrease)
    for i in range(ramp_down):
        work_distribution[ramp_up + peak_duration + i] = 1 - (i + 1) / ramp_down
    
    # Normalize to match total work hours
    work_distribution /= np.sum(work_distribution)
    work_hours_per_day = work_distribution * total_hours  
    
    # Headcount calculation (productivity only affects headcount, not hours)
    total_working_hours_per_day = hours_per_shift * shifts_per_day
    headcount_per_day = (work_hours_per_day / total_working_hours_per_day) / productivity_factor
    
    # Calculate effective duration and end date
    end = work_days[-1]
    effective_duration = duration
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if view == 'Hours':
        ax.bar(work_days, work_hours_per_day, color='b', label='Work Hours', width=0.8)
        ax.set_ylabel("Work Hours")
    else:
        ax.bar(work_days, headcount_per_day, color='r', label='Headcount', width=0.8)
        ax.set_ylabel("Headcount")
    
    ax.set_xlabel("Date")
    ax.set_title("Project Headcount and Work Distribution")
    ax.legend()
    ax.grid()
    
    st.pyplot(fig)
    
    return end.strftime('%Y-%m-%d'), effective_duration, elapsed_days

# Streamlit UI
st.title("Project Headcount Estimator")

start_date = st.date_input("Start Date", value=datetime(2025, 1, 1)).strftime('%Y-%m-%d')
total_hours = st.number_input("Total Work Hours", value=50000, min_value=1)
hours_per_shift = st.number_input("Hours Per Shift", value=10, min_value=1)
shifts_per_day = st.number_input("Shifts Per Day", value=2, min_value=1)
work_days_per_week = st.slider("Working Days Per Week", 1, 7, 6)
productivity_factor = st.slider("Productivity Factor", 0.1, 2.0, 0.8, 0.1)
ramp_up = st.slider("Ramp-Up Duration (Days)", 1, 50, 15)
peak_duration = st.slider("Peak Duration (Days)", 1, 100, 30)
ramp_down = st.slider("Ramp-Down Duration (Days)", 1, 50, 15)

view_option = st.radio("View Mode", ('Hours', 'Headcount'))

if st.button("Estimate Headcount"):
    end_date, duration, elapsed_days = estimate_headcount(start_date, total_hours, hours_per_shift, shifts_per_day, work_days_per_week, productivity_factor, ramp_up, peak_duration, ramp_down, view_option)
    
    st.write(f"**Calculated End Date:** {end_date}")
    st.write(f"**Total Duration:** {duration} effective working days")
    st.write(f"**Elapsed Days:** {elapsed_days} calendar days")
