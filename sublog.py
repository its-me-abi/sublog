import subprocess
import threading
import logging
import sys


class SubprocessLogger:
    """
    Patch subprocess.call to redirect stdout/stderr to Python's logging.
    Works as a context manager for clean enable/disable.
    """

    def __init__(self, log_file="subprocess_output.log", logger_name="subprocess_capture"):
        self.log_file = log_file
        self.logger = logging.getLogger(logger_name)
        self._orig_call = subprocess.call
        self._enabled = False

        # Setup logging handlers once
        if not self.logger.handlers:
            handler_console = logging.StreamHandler(sys.stdout)
            handler_file = logging.FileHandler(log_file, encoding="utf-8")

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler_console.setFormatter(formatter)
            handler_file.setFormatter(formatter)

            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(handler_console)
            self.logger.addHandler(handler_file)

    def _log_stream(self, stream, level):
        """Consume a stream line by line and log it."""
        try:
            for line in iter(stream.readline, b""):
                if not line:
                    break
                self.logger.log(level, line.decode(errors="replace").rstrip())
        finally:
            stream.close()

    def _logging_call(self, *popenargs, **kwargs):
        """Replacement for subprocess.call that logs stdout/stderr."""
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE

        proc = subprocess.Popen(*popenargs, **kwargs)

        threading.Thread(
            target=self._log_stream, args=(proc.stdout, logging.INFO), daemon=True
        ).start()
        threading.Thread(
            target=self._log_stream, args=(proc.stderr, logging.ERROR), daemon=True
        ).start()

        return proc.wait()

    # ---------- Context Manager ----------
    def __enter__(self):
        if not self._enabled:
            subprocess.call = self._logging_call
            self._enabled = True
            self.logger.debug("SubprocessLogger enabled (patched subprocess.call).")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._enabled:
            subprocess.call = self._orig_call
            self._enabled = False
            self.logger.debug("SubprocessLogger disabled (restored subprocess.call).")


if __name__ == "__main__":
    import subprocess  # replace with actual module

    print("Subprocess starting, capture .")
    with SubprocessLogger():
         subprocess.call(["java", "-version"])

    print("Subprocess finished, capture stopped.")
