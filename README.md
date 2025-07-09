# GitLite

**GitLite** is a minimal Git implementation built from scratch in Python to explore and understand the inner workings of Git version control.

---

## Table of Contents

- [🎯 Purpose](#-purpose)
- [📚 References & Inspiration](#-references--inspiration)
- [🛠️ Installation](#%EF%B8%8F-installation)
- [🚀 Usage](#-usage)
- [🧾 Commands](#-commands)
  - [🧱 Command: 'init'](-command-init)
  - [🧱 Command: 'add'](-command-add)
  - [🧱 Command: 'commit'](-command-commit)
- [🧾 Next features / To Do List](#-next-features--to-do-list)
- [🤝 Contributing](#contributing)
- [🪪 License](#license)


---

## 🎯 Purpose

The main goal of this project is educational:

- To **deepen understanding** of how Git works under the hood  
- To **build core Git features** (like `init`, `add`, `commit`, `status`, etc.) from scratch  
- To **learn Python** through real-world, low-level systems programming

---

## 📚 References & Inspiration

This project was heavily inspired in its early stages by the following resources:

- 📘 [Pro Git Book](https://git-scm.com/book/en/v2)  
- 🧩 [WYAG (Write Yourself a Git)](https://wyag.thb.lt/)  
- ✍️ [Build Git From Scratch – Billy Hansweno](https://medium.com/@billyhansweno/building-git-from-scratch-a-journey-into-the-heart-of-version-control-d6c97332cb00)  
- 🔧 [Ugit](https://www.leshenko.net/p/ugit/#)  
- 🐍 [Pygit – Ben Hoyt](https://benhoyt.com/writings/pygit/)

After implementing a few core commands, I shifted to exploring Git directly via its documentation and CLI — aiming to replicate its behavior more accurately through experimentation and hands-on learning.

---

## 🛠️ Installation

To install GitLite locally as a CLI tool:

```bash
git clone https://github.com/rcortes-b/GitLite.git
cd GitLite
pip install .
```

---

## 🚀 Usage

You can use gitlite followed by any of the next commands:
```
  gitlite <command> <...>
```

```markdown
## List of implemented commands

| Command         | Description                                |
|---------------- |--------------------------------------------|
| `init`          | Create a new GitLite repository            |
| `add`           | Add files to staging                       |
| `commit`        | Commit changes                             |
| `status`        | Show repository status                     |
| `ls-files`      | Show files in the index                    |
| `hash-object`   | Compute and store object hashes            |
| `write-tree`    | Write tree from index                      |
| `cat-file`      | Provide details of repository objects      |

```
*Note: In the next section is detailed which features for each command has been implemented

---

## 🧾 Commands

### 🧱 Command: 'init'

Initializes a new GitLite repository by creating the `.gitlite` directory along with the required structure:

- `.gitlite/objects/` – stores all GitLite objects (blobs, trees, commits)  
- `.gitlite/refs/heads/` – stores branch references  
- `.gitlite/config` – stores repository-specific configuration like author and email

Unlike Git, which uses a global config (`~/.gitconfig`), GitLite defines the **author identity per repository** to keep things simple and local — ideal for experimentation without needing centralized identity systems like GitHub.

---

#### 🔧 Usage

| Option     | Description                           |
| ---------- | ------------------------------------- |
| `--author` | Set the name of the repository owner  |
| `--email`  | Set the email of the repository owner |

```bash
gitlite init
```
Creates a .gitlite/ folder in the current directory.
```bash
gitlite init <name>
```
Creates a new folder named <name> and initializes .gitlite/ inside it.
```bash
gitlite init my_repo --author=rcortes- --email=randomemail@email.com
```
All in one init usage


### 🧱 Command: 'add'

The `add` command updates the index with the current content found in the working directory, staging it for the next commit.

- 📄 `.gitlite/index` – The **index file** in GitLite acts as a **staging area**. It tracks which files are staged and ready to be committed.

---

#### 🔧 Usage

| Option     | Description                           |
| ---------- | ------------------------------------- |
| `--all`    | Add all changes from the working tree |

```bash
gitlite add <file> [<file>...]
```
Adds the files given as parameter to the index file or replace the old ones for its new state

```bash
gitlite add --all/ or gitlite add -A
```
Adds all the files found in the working tree to the index file

*Note: Files that are listed in the '.gitliteignore' file are not written in the index file


### 🧱 Command: 'commit'

The `commit` command saves a snapshot of the current index (staged changes) into the GitLite object database. This creates a new commit object pointing to the current tree state and links it to the previous commit (if any).

- 🧾 Each commit stores:
  - A reference to the current tree (from `write-tree`)
  - A parent commit (if it exists)
  - Metadata like author name, email, and date
  - A commit message

---

#### 🔧 Usage

| Option     | Description                             |
| ---------- | --------------------------------------- |
| `-m`       | The commit message which will be stored |

```bash
gitlite commit -m "your commit message"
```

> ⚠️ Unlike Git, GitLite currently supports only the `-m` option and does not track how many files were modified, added, or deleted in the commit.  
> ✅ If the commit is successful, GitLite prints a simple confirmation message.


