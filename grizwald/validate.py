import subprocess


def validate(path, validator, scrape=False):
    cmd = ["./addon-validator", path, "--determined", "-o", "json"]
    if scrape:
        cmd.append("--scrape")
    shell = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE,
                             cwd=validator)
    data, stderr = shell.communicate()
    return data
