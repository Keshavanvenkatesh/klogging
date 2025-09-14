import datetime
import os

class logger:

    logger_name_list = []
    dupilicate_logger_counter = 1
    can_i_write_logs = True

    def __init__(self, name, max_size=1048576):  # default 1 MB
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

    def logging(self, file_to_log="logging.txt"):
        """Decorator to log function calls"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                timestamp = datetime.datetime.now()
                function_name = func.__name__
                arguments = [arg for arg in args]
                
                try:
                    result = func(*args, **kwargs)
                    log = f"[NO ERROR] {timestamp} >>> logger:{self.name}>>> function: {function_name}({arguments}) :return({result}): no error"
                except Exception as e:
                    result = None
                    log = f"[ERROR] {timestamp} >>> logger:{self.name}>>> function: {function_name}({arguments}) :return(none): {type(e).__name__} - {e}"

                # rotate before writing
                logger.rotate_log(file_to_log, self.max_size)

                if self.can_i_write_logs and not logger.is_log_full(file_to_log, self.max_size):
                    with open(file_to_log, "a") as file:
                        file.write(log + "\n\n")
                elif not self.can_i_write_logs:
                    print(f"logger {self.name} is turned off")
                elif not logger.can_i_write_logs:
                    print("all logs are turned off")
                else:
                    logger.handle_log_full(log)

                return result
            return wrapper
        return decorator

    def log_info(self, msg, PREFIX="\t", POSTFIX="", file_to_log="logging.txt"):
        """Write manual info logs"""
        logger.rotate_log(file_to_log, self.max_size)

        content = PREFIX + "[INFO] " + str(self.name) + " >>> " + msg + " " + POSTFIX
        if logger.is_log_full(file_to_log, self.max_size):
            logger.handle_log_full(content)
        else:
            with open(file_to_log, "a") as file:
                file.write(content + "\n")

    def show_logs(self, log_file="logging.txt"):
        """Display logs for this logger"""
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

        print("="*int((max_length-len(start_of_log))/2) + start_of_log + "="*int((max_length-len(start_of_log))/2))
        logger_name_in_file = f"logger:{self.name}"
        for line in lines:
            if logger_name_in_file in line:
                print(line.strip())
        print("="*int((max_length-len(end_of_log))/2) + end_of_log + "="*int((max_length-len(end_of_log))/2))

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

        print("="*int((max_length-len(start_of_log))/2) + start_of_log + "="*int((max_length-len(start_of_log))/2))
        for line in lines:
            print(line.strip())
        print("="*int((max_length-len(end_of_log))/2) + end_of_log + "="*int((max_length-len(end_of_log))/2))

    @classmethod
    def show_logger(cls):
        """Show all created loggers"""
        for logger_item in cls.logger_name_list:
            print(logger_item)

    @classmethod
    def check_logger_duplicate_name(cls, new_logger_name):
        return new_logger_name in cls.logger_name_list
    
    @staticmethod
    def handle_log_full(content):
        print("=================== LOG IS FULL ===================")
        print(content)
        print("===================================================")

    @staticmethod
    def is_log_full(file="logging.txt", max_size=1048576):
        size = os.path.getsize(file) if os.path.exists(file) else 0
        return size >= max_size
    
    @staticmethod
    def rotate_log(file="logging.txt", max_size=1048576):
        """Rotate the log file if it exceeds max_size"""
        if os.path.exists(file) and os.path.getsize(file) >= max_size:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{file}_{timestamp}.bak"
            os.rename(file, new_name)
            print(f"🔄 Log rotated: {new_name}")

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
        print("""
🔹 Logger Class Help 🔹
- Logs function calls, arguments, return values, and errors
- Manual log messages
- Turn logs ON/OFF per logger or globally
- View logs for one logger or all
- Automatic file rotation when log file exceeds size limit

Usage:
    logger_instance = logger('my_logger', max_size=2048)

    @logger_instance.logging()
    def add(a, b):
        return a + b

Methods:
 - logging(file_to_log="logging.txt") → Decorator for logging function calls
 - log_info(msg, PREFIX="\\t", POSTFIX="", file_to_log="logging.txt") → Manual info
 - show_logs(log_file="logging.txt") → Show logs for this logger
 - show_all_logs(log_file="logging.txt") → Show all logs
 - show_logger() → Show all created loggers
 - turn_on_log() / turn_off_log() → Enable/disable logging for this logger
 - turn_on_all_logs() / turn_off_all_logs() → Enable/disable all loggers
 - rotate_log(file="logging.txt", max_size=N) → Rotate file if it exceeds N bytes
 - help() → Show this help
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