from datetime import datetime


def validate_time_units(unit, valid_units):
    if unit not in valid_units:
        raise ValueError(f"Invalid time unit '{unit}'. Supported units are: {', '.join(valid_units)}")

def get_date_time_simulation_data(simulation_config: dict) -> tuple[datetime, int, int]:
    # Extract the start date/time and formatting string from the configuration.
    start_date_time = simulation_config.get('start_date_time')
    start_date_time_format = simulation_config.get('start_date_time_format')
    start_date_time = datetime.strptime(start_date_time, start_date_time_format)

    # Define conversion factors for various time units to seconds.
    unit_to_seconds = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400,
        "week": 604800,
        "month": 30 * 86400,  # Approximation for a month
        "year": 365 * 86400,  # Approximation for a year
    }

    # Extract the simulation duration and its unit from the configuration.
    duration = simulation_config.get('duration')
    time_unit = simulation_config.get('time_unit')
    validate_time_units(time_unit, unit_to_seconds.keys())
    # Convert the simulation duration into seconds.
    sim_duration = unit_to_seconds.get(time_unit.lower(), 1) * duration

    # Extract the sample unit and convert it to seconds, defaulting to 1 second if unknown.
    sample_unit = simulation_config.get('sample_unit')
    validate_time_units(sample_unit, unit_to_seconds.keys())
    sampling_rate = unit_to_seconds.get(sample_unit.lower(), 1)  # Default to 1 second if unit is unknown

    # Return the formatted start date/time, total simulation duration, and sampling rate.
    return start_date_time, sim_duration, sampling_rate