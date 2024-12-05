from datetime import datetime, timezone
import os


def error_log(message, error):
    try:
        utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

        # Get ARTISAN_STOCK_CHECKER_CONFIG_DIR from environment or default to local path
        config_dir = os.environ.get('ARTISAN_STOCK_CHECKER_CONFIG_DIR', '.')

        # Ensure the logs directory exists
        logs_dir = os.path.join(config_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Construct the log file path
        log_file_path = os.path.join(logs_dir, f"{utc_time}_error_log.txt")

        with open(log_file_path, "a") as log_file:
            log_file.write(utc_time + ", ")
            log_file.write(message + ", ")
            log_file.write(str(error).replace("\n", "\\n"))
            log_file.write("\n")
        print(message)
        print(str(error).replace("\n", "\\n"))
    except Exception as e:
        print("Could not write to error log:")
        print(e)
