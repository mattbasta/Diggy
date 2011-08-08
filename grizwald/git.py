import subprocess


def _run_command(cmd, repo):
    """Run a shell command in a particular directory."""
    pipe = subprocess.Popen(cmd, shell=True, cwd=repo, stdout=subprocess.PIPE)
    data, stderr_data = pipe.communicate()
    return data


def git_pull(remote="origin", branch="master", repo=None):
    """Perform a git pull on a repo."""
    if not repo:
        return
    _run_command("git pull -f %s %s" % (remote, branch), repo)


def git_reset_hard(commit, repo):
    """Perform a git reset --hard on a repo."""
    _run_command("git reset --hard %s" % commit, repo)


def git_get(repo, commit):
    """Gets a dict of data about the commit."""
    output = _run_command(
            'git log %s^1..%s --pretty=format:"%%H %%ct"' % (commit, commit),
            repo)
    return output.split()

