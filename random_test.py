import threading
import sys
from io import StringIO


class ThreadWithCustomOutput(threading.Thread):
    def __init__(self, target=None, args=(), kwargs={}):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.output_stream = StringIO()  # Create a custom output stream for each thread
        self.original_stdout = sys.stdout

    def run(self):
        # Redirect stdout to the custom output stream
        sys.stdout = self.output_stream
        super().run()
        # Restore the original stdout
        sys.stdout = self.original_stdout

    def get_output(self):
        return self.output_stream.getvalue()


def thread_function(thread_id):
    print(f"This is thread {thread_id}")


# Create and start multiple threads
threads = []
for i in range(3):
    thread = ThreadWithCustomOutput(target=thread_function, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Get and display output from each thread
for i, thread in enumerate(threads):
    thread_output = thread.get_output()
    print(f"Output from thread {i}:")
    print(thread_output)
