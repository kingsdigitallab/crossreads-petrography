from pathlib import Path
import pytest

TEST_DIR = Path(__file__).parent.parent / "tests"

def test():
    testcmd = ["-v", "--disable-warnings", str(TEST_DIR)]
    try:
        exit_code = pytest.main(testcmd)
        print(f"Pytest exit code: {exit_code}")
        return exit_code == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False