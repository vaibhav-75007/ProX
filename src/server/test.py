"""Contains testing functions following the Test-Driven Development approach"""

import json
from Server import Server

IP = "127.0.0.1"  # Local server's IP
PORT = 10000  # Local server's port

def create_test_db():
    """Create some data for the test database. Returns the db's path"""
    test_db = "test.json"
    # TODO
    return test_db

db_path = create_test_db()
server = Server(IP, PORT, db_path)

def test_run_server():
    raise NotImplementedError("You suck")

def test_send_message_receive_response():
    raise NotImplementedError

def test_load_db():
    raise NotImplementedError

def test_update_db():
    raise NotImplementedError

def test_memory_freed_after_idling():
    raise NotImplementedError

def test_add_user():
    raise NotImplementedError

def test_add_task():
    raise NotImplementedError

def test_add_flashcard():
    raise NotImplementedError

TESTS = [
    test_run_server,
    test_send_message_receive_response,
    test_load_db,
    test_update_db,
    test_memory_freed_after_idling,
    test_add_user,
    test_add_task,
    test_add_flashcard
]

colors = dict(
    HEADER = '\033[95m',
    OKBLUE = '\033[94m',
    OKCYAN = '\033[36m',
    OKGREEN = '\033[92m',
    WARNING = '\033[93m',
    FAIL = '\033[91m',
    ENDC = '\033[0m',
    BOLD = '\033[1m',
    UNDERLINE = '\033[4m'
)  # Color codes from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python

def run_tests():
    for test_func in TESTS:
        name = test_func.__name__
        print(f">>> Testing method {colors['OKBLUE']}{name}{colors['ENDC']}: ", end='')
        try:
            test_func()
            print(f"{colors['OKGREEN']} PASSED{colors['ENDC']}.", end='\n\n')
        except Exception as e:
            print(f"{colors['FAIL']} FAILED{colors['ENDC']}")
            print(f"Exception raised: {colors['FAIL']}{e}{colors['ENDC']}", end='\n\n')
            return


if __name__ == "__main__":
    run_tests()