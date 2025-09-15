from datetime import datetime
import os

class logger:

    logger_name_list = []
    dupilicate_logger_counter = 1
    can_i_write_logs = True

    def __init__(self, name, max_size=1048576, file_to_log="logging.txt"):  # default 1 MB
        base_name = str(name)

        if logger.check_logger_duplicate_name(base_name):
            unique_name = base_name + str(logger.dupilicate_logger_counter)
            logger.dupilicate_logger_counter += 1
            self.name = unique_name
        else:
            self.name = base_name

        logger.logger_name_list.append(self.name)
        self.can_i_write_logs = True
        self.max_size = max_size
        self.file_to_log = file_to_log

    # ---------------------- Helper Methods ----------------------

    @staticmethod
    def _get_timestamp():
        """Current timestamp string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def is_log_full(file="logging.txt", max_size=1048576):
        size = os.path.getsize(file) if os.path.exists(file) else 0
        return size > max_size   # changed from >=

    @staticmethod
    def rotate_log(file="logging.txt", max_size=1048576):
        """Rotate the log file if it exceeds max_size"""
        if os.path.exists(file) and os.path.getsize(file) > max_size:  # changed from >=
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            new_name = f"{file}_{timestamp}.bak"
            os.rename(file, new_name)
            print(f"🔄 Log rotated: {new_name}")


    @staticmethod
    def handle_log_full(content):
        print("=================== LOG IS FULL ===================")
        print(content)
        print("===================================================")

    # ---------------------- Decorator ----------------------

    def logging(self, file_to_log="logging.txt"):
        def decorator(func):
            def wrapper(*args, **kwargs):
                timestamp = logger._get_timestamp()
                function_name = func.__name__
                arguments = [arg for arg in args]

                try:
                    result = func(*args, **kwargs)
                    log = (f"[NO ERROR] {timestamp} >>> logger:{self.name} "
                           f">>> function:{function_name}({arguments}) "
                           f":return({result}): no error")
                except Exception as e:
                    result = None
                    log = (f"[ERROR] {timestamp} >>> logger:{self.name} "
                           f">>> function:{function_name}({arguments}) "
                           f":return(None): {type(e).__name__} - {e}")

                # Rotate if full
                if logger.is_log_full(file_to_log, self.max_size):
                    logger.rotate_log(file_to_log, self.max_size)

                # Write log
                if self.can_i_write_logs and logger.can_i_write_logs:
                    if logger.is_log_full(file_to_log, self.max_size):
                        logger.handle_log_full(log)
                    else:
                        with open(file_to_log, "a") as file:
                            file.write(log + "\n\n")

                return result
            return wrapper
        return decorator

    # ---------------------- Manual Logs ----------------------

    def log_info(self, msg, function_name="unknown", arguments="[None]", return_value="None",
                 PREFIX="\t", POSTFIX="", file_to_log="logging.txt"):
        """Write manual info log"""
        if logger.is_log_full(file_to_log, self.max_size):
            logger.rotate_log(file_to_log, self.max_size)

        timestamp = logger._get_timestamp()
        content = (f"{PREFIX}[INFO] {timestamp} >>> logger:{self.name} "
                   f">>> function:{function_name}({arguments}) "
                   f":return({return_value}): {msg} {POSTFIX}")

        if logger.is_log_full(file_to_log, self.max_size):
            logger.handle_log_full(content)
        else:
            with open(file_to_log, "a") as file:
                file.write(content + "\n")

    def log_warning(self, msg, function_name="unknown", arguments="[None]", return_value="None",
                    PREFIX="\t", POSTFIX="", file_to_log="logging.txt"):
        """Write manual warning log"""
        if logger.is_log_full(file_to_log, self.max_size):
            logger.rotate_log(file_to_log, self.max_size)

        timestamp = logger._get_timestamp()
        content = (f"{PREFIX}[WARNING] {timestamp} >>> logger:{self.name} "
                   f">>> function:{function_name}({arguments}) "
                   f":return({return_value}): {msg} {POSTFIX}")

        if logger.is_log_full(file_to_log, self.max_size):
            logger.handle_log_full(content)
        else:
            with open(file_to_log, "a") as file:
                file.write(content + "\n")

    def log_error(self, msg, function_name="unknown", arguments="[None]", return_value="None",
                  PREFIX="\t", POSTFIX="", file_to_log="logging.txt"):
        """Write manual error log"""
        if logger.is_log_full(file_to_log, self.max_size):
            logger.rotate_log(file_to_log, self.max_size)

        timestamp = logger._get_timestamp()
        content = (f"{PREFIX}[ERROR] {timestamp} >>> logger:{self.name} "
                   f">>> function:{function_name}({arguments}) "
                   f":return({return_value}): {msg} {POSTFIX}")

        if logger.is_log_full(file_to_log, self.max_size):
            logger.handle_log_full(content)
        else:
            with open(file_to_log, "a") as file:
                file.write(content + "\n")

    # ---------------------- Log Viewing ----------------------

    def show_logs(self, log_file="logging.txt"):
        """Display logs for this logger only"""
        if not os.path.exists(log_file):
            print("THE LOG IS EMPTY !!!")
            return

        with open(log_file) as file:
            lines = file.readlines()

        if not lines:
            print("THE LOG IS EMPTY !!!")
            return

        max_length = max(len(line) for line in lines)
        start_of_log = " start of log "
        end_of_log = " end of log "

        print("=" * int((max_length - len(start_of_log)) / 2) + start_of_log + "=" * int((max_length - len(start_of_log)) / 2))
        logger_name_in_file = f"logger:{self.name}"
        for line in lines:
            if logger_name_in_file in line:
                print(line.strip())
        print("=" * int((max_length - len(end_of_log)) / 2) + end_of_log + "=" * int((max_length - len(end_of_log)) / 2))

    @staticmethod
    def show_all_logs(log_file="logging.txt"):
        """Display all logs"""
        if not os.path.exists(log_file):
            print("THE LOG IS EMPTY !!!")
            return

        with open(log_file) as file:
            lines = file.readlines()

        if not lines:
            print("THE LOG IS EMPTY !!!")
            return

        max_length = max(len(line) for line in lines)
        start_of_log = " start of log "
        end_of_log = " end of log "

        print("=" * int((max_length - len(start_of_log)) / 2) + start_of_log + "=" * int((max_length - len(start_of_log)) / 2))
        for line in lines:
            print(line.strip())
        print("=" * int((max_length - len(end_of_log)) / 2) + end_of_log + "=" * int((max_length - len(end_of_log)) / 2))
        
######################################################################################################################
    @staticmethod
    def show_all_error(log_file="logging.txt"):
        """Display all error logs"""
        if not os.path.exists(log_file):
            print("THE LOG IS EMPTY !!!")
            return

        with open(log_file) as file:
            lines = file.readlines()

        if not lines:
            print("THE LOG IS EMPTY !!!")
            return

        max_length = max(len(line) for line in lines if "[ERROR]" in line)
        start_of_log = " start of log "
        end_of_log = " end of log "

        print("=" * int((max_length - len(start_of_log)) / 2) + start_of_log + "=" * int((max_length - len(start_of_log)) / 2))
        for line in lines:
            if "[ERROR]" in line:
                print(line.strip())
            else:
                pass
        print("=" * int((max_length - len(end_of_log)) / 2) + end_of_log + "=" * int((max_length - len(end_of_log)) / 2))
    
    @staticmethod
    def show_all_warning(log_file="logging.txt"):
        """Display all error logs"""
        if not os.path.exists(log_file):
            print("THE LOG IS EMPTY !!!")
            return

        with open(log_file) as file:
            lines = file.readlines()

        if not lines:
            print("THE LOG IS EMPTY !!!")
            return

        max_length = max(len(line) for line in lines if "[WARNING]" in line)
        start_of_log = " start of log "
        end_of_log = " end of log "

        print("=" * int((max_length - len(start_of_log)) / 2) + start_of_log + "=" * int((max_length - len(start_of_log)) / 2))
        for line in lines:
            if "[WARNING]" in line:
                print(line.strip())
            else:
                pass
        print("=" * int((max_length - len(end_of_log)) / 2) + end_of_log + "=" * int((max_length - len(end_of_log)) / 2))
    
    @staticmethod
    def show_all_info(log_file="logging.txt"):
        """Display all error logs"""
        if not os.path.exists(log_file):
            print("THE LOG IS EMPTY !!!")
            return

        with open(log_file) as file:
            lines = file.readlines()

        if not lines:
            print("THE LOG IS EMPTY !!!")
            return

        max_length = max(len(line) for line in lines if "[INFO]" in line)
        start_of_log = " start of log "
        end_of_log = " end of log "

        print("=" * int((max_length - len(start_of_log)) / 2) + start_of_log + "=" * int((max_length - len(start_of_log)) / 2))
        for line in lines:
            if "[INFO]" in line:
                print(line.strip())
            else:
                pass
        print("=" * int((max_length - len(end_of_log)) / 2) + end_of_log + "=" * int((max_length - len(end_of_log)) / 2))
############################################################################################################################

    # ---------------------- Logger Management ----------------------

    @classmethod
    def show_logger(cls):
        """Show all created loggers"""
        for logger_item in cls.logger_name_list:
            print(logger_item)

    @classmethod
    def check_logger_duplicate_name(cls, new_logger_name):
        return new_logger_name in cls.logger_name_list

    def turn_on_log(self):
        self.can_i_write_logs = True

    def turn_off_log(self):
        self.can_i_write_logs = False

    @classmethod
    def turn_off_all_logs(cls):
        cls.can_i_write_logs = False

    @classmethod
    def turn_on_all_logs(cls):
        cls.can_i_write_logs = True


    @staticmethod
    def help():
        print(r"""
🔹 Logger Class Help 🔹
A custom Python logger with support for:
- Automatic logging of function calls (decorators)
- Error capturing with full trace of arguments/return values
- Manual log entries: INFO, WARNING, ERROR
- Log viewing (per logger, all logs, or filtered by level)
- Automatic file rotation when log size exceeds a limit
- Per-logger and global log ON/OFF switching

📌 Basic Usage:
    my_logger = logger("example_logger", max_size=2048)  # 2 KB rotation

    @my_logger.logging()
    def add(a, b):
        return a + b

    add(5, 2)  # auto-logged
    my_logger.log_info("Manual info message")
    my_logger.log_warning("Manual warning")
    my_logger.log_error("Manual error")

🧰 Methods:
 - logging(file_to_log="logging.txt")   
       → Decorator: auto-log function calls, args, return values, errors

 - log_info(msg, ..., file_to_log="logging.txt")   
       → Manual info log with timestamp, args, return value
 - log_warning(msg, ..., file_to_log="logging.txt")   
       → Manual warning log
 - log_error(msg, ..., file_to_log="logging.txt")   
       → Manual error log

 - show_logs(log_file="logging.txt")   
       → Display logs for this logger only
 - show_all_logs(log_file="logging.txt") [static]   
       → Display all logs
 - show_all_info(log_file="logging.txt") [static]   
       → Display only INFO logs
 - show_all_warning(log_file="logging.txt") [static]   
       → Display only WARNING logs
 - show_all_error(log_file="logging.txt") [static]   
       → Display only ERROR logs

 - show_logger() [class]   
       → Show all created logger names

 - turn_on_log() / turn_off_log()   
       → Enable/disable this logger
 - turn_on_all_logs() / turn_off_all_logs() [class]   
       → Enable/disable all loggers

 - rotate_log(file="logging.txt", max_size=N) [static]   
       → Rotate log file when it exceeds N bytes (renames with timestamp)

🧠 Notes:
 - Default log file: `logging.txt`
 - Default max size: `1 MB` (1048576 bytes), can be changed per logger
 - Duplicate names get numeric suffixes (logger1, logger2, …)
 - Logs include: timestamp, logger name, function, arguments, return, and error details
 - Rotation renames the full log file with a `.bak` timestamp and starts a new one

👉 Call `logger.help()` anytime to show this guide.
""")

# =================== Example Usage ===================

if __name__ == "__main__":
    # Create a logger with 1 KB max file size for testing rotation
    my_logger = logger("example_logger", max_size=1024)

    @my_logger.logging()
    def add(a, b):
        return a + b

    @my_logger.logging()
    def divide(a, b):
        return a / b

    add(5, 3)
    divide(10, 2)
    divide(5, 0)  # will log ZeroDivisionError
    my_logger.log_info("This is a manual info log.")

    print("\n--- Logs for this logger ---")
    my_logger.show_logs()

    print("\n--- All logs ---")
    logger.show_all_logs()