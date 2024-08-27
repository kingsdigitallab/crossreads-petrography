from . import *
TEST_DIR = Path(__file__).parent.parent / "tests"

def run_tests(verbosity_str="q"):
    import pytest
    testcmd = [f"-{verbosity_str}", "--disable-warnings", str(TEST_DIR)]
    logger.setLevel(logging.ERROR)
    try:
        exit_code = pytest.main(testcmd)
        return exit_code == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
