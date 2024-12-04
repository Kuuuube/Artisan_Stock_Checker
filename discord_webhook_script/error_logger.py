from datetime import datetime, timezone
import os


def error_log(message, error):
    try:
        # Get the current UTC time
        utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

        # Get CONFIG_PATH from environment or default to local path
        config_path = os.environ.get('CONFIG_PATH', '.')

        # Ensure the logs directory exists
        logs_dir = os.path.join(config_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Construct the log file path
        log_file_path = os.path.join(logs_dir, f"{utc_time}_error_log.txt")

        # Write the error message to the log file
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{utc_time}, ")
            log_file.write(f"{message}, ")
            log_file.write(str(error).replace("\n", "\\n"))
            log_file.write("\n")

        # Print the error message to the console
        print(message)
        print(str(error).replace("\n", "\\n"))
    except FileNotFoundError | Exception as e:
        print("Could not write to error log:")
        print(e)
