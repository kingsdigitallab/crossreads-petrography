from . import *
TEST_DIR = Path(__file__).parent.parent / "tests"

def run_tests(verbosity_str="q"):
    import pytest
    testcmd = [f"-{verbosity_str}", "--disable-warnings", str(TEST_DIR)]
    logger.info(f"Running tests with verbosity: {verbosity_str}")
    logger.setLevel(logging.CRITICAL + 1)
    try:
        exit_code = pytest.main(testcmd)
        if exit_code == 0:
            logger.info("\nAll tests passed")
            return True
        else:
            logger.error("\nSome tests failed")
            return False
    except Exception as e:
        logger.error(f"Testing error: {e}")
        return False