"""
Contains unit testing functions following the Test-Driven Development approach.
Start the server first by running main.py before running the tests below
"""

import json

SERVER = '127.0.0.1'
PORT = 54321
URL = f'http://{SERVER}:{PORT}'

def create_test_db():
    """
    Create some data for the test database. Returns the db's path
    """
    test_db = "test.json"
    return test_db

tests = list()

def unit_test(test_func):
    """
    Decorator for each unit testing function
    """
    global tests
    tests.append(test_func)
    def run():
        test_func()
    return run

colors = dict(
    OKBLUE = '\033[94m',
    OKGREEN = '\033[92m',
    FAIL = '\033[91m',
    ENDC = '\033[0m',
)  # Color codes from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python

def run_tests():
    for test_func in tests:
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