# hosted on gist at: https://gist.githubusercontent.com/quadrismegistus/aee85e466a542c347f90a2a0237752da/raw/crossreads_petrography_installer.py

import os
import sys
import subprocess
import logging
from contextlib import contextmanager
from io import StringIO

INSTALLED = False
REPO_NAME = "crossreads-petrography"
REPO_URL = f"https://github.com/kingsdigitallab/{REPO_NAME}.git"


@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout.getvalue(), sys.stderr.getvalue()
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[0;36m',  # Cyan
        'INFO': '\033[0;32m',   # Green
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',   # Red
        'CRITICAL': '\033[0;35m',  # Magenta
        'RESET': '\033[0m',      # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

def setup_logger():
    logger = logging.getLogger('crossreads_petrography')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Prevent propagation to root logger

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger()


def run_command(command, quiet=False):
    with capture_output() as (out, err):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        )
        output, error = process.communicate()
        if process.returncode != 0 and not quiet:
            logger.error(f"Error running {command}:\n\n{error}")
            return False
    return True


def github_auth_clone(persistent_key: bool):
    """
    Authenticate with GitHub to access private repo. This function will
    detect if there is `id_ed25519` key SSH profile. If not, it will create
    one.
    - `persistent_key`: Store private key in Google Drive.

    from: https://raw.githubusercontent.com/tsunrise/colab-github/main/colab_github.py
    """
    import os
    os.system("mkdir -p ~/.ssh")
    if persistent_key:
        from google.colab import drive
        if not os.path.exists("/content/drive/"):
            logger.info("Mounting Google Drive")
            drive.mount("/content/drive/")
        else:
            logger.info("Google Drive already mounted")
        private_key_dir = "/content/drive/MyDrive/.colab-github"
        os.system(f"mkdir -p {private_key_dir}")
    else:
        private_key_dir = "~/.ssh"

    private_key_path = private_key_dir + "/id_ed25519"
    public_key_path = private_key_path + ".pub"

    if not os.path.exists(os.path.expanduser(private_key_path)):
        fresh_key = True
        os.system(f"ssh-keygen -t ed25519 -f {private_key_path} -N ''")
    else:
        fresh_key = False

    if persistent_key:
        os.system("rm -f ~/.ssh/id_ed25519")
        os.system("rm -f ~/.ssh/id_ed25519.pub")
        os.system(f"cp -s {private_key_path} ~/.ssh/id_ed25519")
        os.system(f"cp -s {public_key_path} ~/.ssh/id_ed25519.pub")


    with open(os.path.expanduser(public_key_path), "r") as f:
        public_key = f.read()
    
    key_error_msg = f"Please go to https://github.com/settings/ssh/new to upload the following key:\n{public_key}"
    if fresh_key:
        logger.warning(key_error_msg)

    # add github to known hosts (you may hardcode it to prevent MITM attacks)
    os.system("ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts")
    os.system("chmod go-rwx ~/.ssh/id_ed25519")

    # Set repository address and name
    repo_name = REPO_NAME
    repo_addr = REPO_URL

    # Clone repository only if it doesn't exist
    if not os.path.exists(repo_name):
        logger.info(f"Cloning repository {repo_name}")
        if not run_command(f"git clone {repo_addr}"):
            logger.warning(key_error_msg)
            return False
        logger.info(f"Cloned repository {repo_name}")
    else:
        logger.info(f"Pulling repository {repo_name}")
        if not run_command(f"cd {repo_name} && git pull -q && cd .."):
            logger.warning(key_error_msg)
            return False
        logger.info(f"Pulled repository {repo_name}")

    # Install requirements
    logger.info(f"Installing requirements for {repo_name}")
    if not run_command(f"pip install -q -r {repo_name}/requirements.txt"):
        return False
    logger.info(f"Installed requirements for {repo_name}")

    # Add repository to Python path
    repo_path = os.path.abspath(repo_name)
    if repo_path not in sys.path:
        sys.path.append(os.path.abspath(repo_name))
        logger.info(f"Added {repo_name} to Python path")

    return True

def test_import():
    # test import
    try:
        import crossreads_petrography
        logger.info(f"Installation of crossreads_petrography version {crossreads_petrography.__version__} successful.")
        return True
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False


def run_tests():
    if run_command("pip install -q pytest"):
        if run_command(f"pytest {REPO_NAME}/tests"):
            logger.info("All tests passed.")
            return True
        else:
            logger.error("Tests failed.")
            return False
    else:
        return False


def install(persistent_key: bool = True):
    # clone repo
    if not github_auth_clone(persistent_key=persistent_key):
        return
    # test import
    if not test_import():
        return
    # run tests
    if not run_tests():
        return
    

if __name__ == "__main__":
    if install():
        INSTALLED = True
