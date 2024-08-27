from . import *
TEST_DIR = Path(__file__).parent.parent / "tests"

def run_tests():
    import pytest
    testcmd = ["-v", "--disable-warnings", str(TEST_DIR)]
    try:
        exit_code = pytest.main(testcmd)
        return exit_code == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
