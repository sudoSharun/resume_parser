import logging

class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger('resume_parser')  # Unique logger name
        self.logger.setLevel(logging.INFO)

        if not self.logger.hasHandlers():
            file_handler = logging.FileHandler('app.log')
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message) -> None:
        self.logger.info(f"{message}")

    def error(self, message) -> None:
        self.logger.error(f"{message}")

    def warning(self, message) -> None:
        self.logger.warning(f"{message}")

log = Logger()