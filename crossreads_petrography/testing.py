from . import *
TEST_DIR = Path(__file__).parent.parent / "tests"

def run_tests(verbosity_str="q"):
    import pytest
    testcmd = [f"-{verbosity_str}", "--disable-warnings", str(TEST_DIR)]
    logger.setLevel(logging.CRITICAL + 1)
    try:
        exit_code = pytest.main(testcmd)
        logger.setLevel(logging.INFO)
        return exit_code == 0
    except Exception as e:
        logger.setLevel(logging.INFO)
        logger.error(f"Testing error: {e}")
        return False