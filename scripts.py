import subprocess


def test():
    subprocess.run("pytest")


def format():
    subprocess.run(["ruff", "check", "--fix"])
    subprocess.run(["ruff", "format"])
