# GitRepo
It is quite boring everytime typing `git init` in your local computer then go to github and initialize a new repository, take the remote url and add it to the local... I am already tired just by explaining. Thanks God **GitRepo** exists. <br/>
Gitrepo is a command-line application that automates initializing a new repository both locally and on GitHub. The user can either initialize the repository in the directory they are currently working in, or generate a brand new folder which will come initialized as a git and github repository.

## Installation

```
$ git clone https://github.com/silverhairs/gitrepo.git
$ cd GitRepo/
$ pip install --editable .
```
## Usage
- Run `gitrepo` to initilize a new repository in a new folder. The folder should come with a README.md file auto-generated by github. <br/>
- Run `gitrepo here` to initialize a new git and github repository on your current directory. All the files in the current directory will be added and pushed to github.