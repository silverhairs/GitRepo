#!/usr/bin/env  python3
import click
import os
import sys
import git
from github import Github

BOLD_TEXT = "\033[1m"


@click.group()
@click.version_option(version="1.0.3")
def main():
    """
    A CLI tool to initialize a repository both locally and on GitHub
    """


@main.command()
@click.option("--username", "-u", prompt=True, help="Enter your github username")
@click.option(
    "--password", "-p", prompt=True, help="Enter your github password", hide_input=True
)
@click.option("--name", "-n", prompt=True, help="Enter repository name")
def new(username, password, name):
    """
    Generate a new Github repository folder in the current location
    """
    user = Github(username, password).get_user()
    
    private = click.confirm("Should the repository be private?")
    desc = click.prompt("Description ", default="")

    try:
        click.secho(f"{BOLD_TEXT}Creating repository {name} ...", fg="blue")
        user.create_repo(
            name=name, description=desc, private=private, auto_init=True,
        )
        # Clone repo in current directory
        url = user.get_repo(name).clone_url
        git.Git(os.getcwd()).clone(url)
        click.secho(f"{BOLD_TEXT}Repository successfully created! 🔥️🔥️", fg="green")
    except Exception as e:
        click.secho(f"{repr(e)}", fg="red")


@main.command()
@click.option("--username", "-u", prompt=True, help="Enter your github username")
@click.option(
    "--password", "-p", prompt=True, help="Enter your github password", hide_input=True
)
def here(username, password):
    """
    Initialize the current directory as a git and github repository
    """
    user = Github(username, password).get_user()
    cwd = os.getcwd()  # current working directory
    cwd_name = os.path.basename(cwd)  # current folder name

    # Check if there is a .gitignore file
    if not os.path.exists(".gitignore"):
        gitignore_status = click.confirm(
            f"{BOLD_TEXT}We detect no gitignore file in your project do you want to continue anyway?",
            abort=True,
        )

    private = click.confirm("Should the repository be private?")
    desc = click.prompt("Description ", default="")

    try:
        click.secho(f"{BOLD_TEXT}Creating repository {cwd_name}...", fg="blue")
        user.create_repo(
            name=cwd_name, description=desc, private=private,
        )
        url = user.get_repo(cwd_name).clone_url

    except Exception as e:
        click.secho(f"{BOLD_TEXT}{repr(e)}", bg="red")
        sys.exit("Aborted!")

    repo = git.Repo.init(path=cwd)
    remote = repo.create_remote(name="origin", url=url)

    # Add and commit files
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for f in files:
        repo.index.add([f"{cwd}/{f}"])
    commit_msg = click.prompt("Commit message ", default="Initial commit")
    repo.index.commit(message=commit_msg)

    # Push to github.com in master branch
    try:
        remote.push(refspec="master:master")
        click.secho(
            f"{BOLD_TEXT}Respo {cwd_name} successfully created locally! 🔥️🔥️",
            fg="green",
        )
    except Exception as e:
        click.secho(f"{repr(e)}", fg="red")
        sys.exit("Aborted!")
