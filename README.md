# GitLite

**GitLite** is a minimal Git implementation built from scratch in Python to explore and understand the inner workings of Git version control.

---

## Table of Contents

- [🎯 Purpose](#-purpose)
- [📚 References & Inspiration](#-references--inspiration)
- [🛠️ Installation](#%EF%B8%8F-installation)
- [🚀 Usage](#-usage)
- [🧾 Commands](#-commands)
  - [🧱 Command: 'init'](#-command-init)
  - [🧱 Command: 'add'](#-command-add)
  - [🧱 Command: 'commit'](#-command-commit)
  - [🧱 Command: 'status'](#-command-status)
  - [🧱 Command: 'ls-files'](#-command-ls-files)
  - [🧱 Command: 'hash-object'](#-command-hash-object)
  - [🧱 Command: 'write-tree'](#-command-write-tree)
  - [🧱 Command: 'cat-file'](#-command-cat-file)
- [🧾 Next features / To Do List](#-next-features--to-do-list)
- [🤝 Contributing](#-contributing)


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

### 🧱 Command: `init`

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
Creates a .gitlite/ directory in the current directory.
```bash
gitlite init <name>
```
Creates a new directory named <name> and initializes .gitlite/ inside it.
```bash
gitlite init my_repo --author=rcortes- --email=randomemail@email.com
```
All in one init usage

---

### 🧱 Command: `add`

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

---

### 🧱 Command: `commit`

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

---

### 🧱 Command: `status`

This command shows the state of the working directory and the index. It lets you see which changes have been staged, which haven’t, and which files aren’t being tracked by GitLite.

Unlike Git, this implementation keeps it minimal — it shows:

- ✅ Staged files (files added to the index)
- 📝 Modified files (changed in the working directory but not staged)
- ❌ Deleted files (removed from the working directory but still in index)
- ➕ Untracked files (not in index at all)

---

#### 🔧 Usage

```bash
gitlite status
```

---

### 🧱 Command: `ls-files`

This command displays information about files that are tracked by GitLite, as well as the status of files that have been deleted, modified, or are untracked.

It works similarly to Git’s `ls-files` command and is useful for inspecting the contents of the GitLite index and working directory.

---

#### 🔧 Usage

| Option / Flag      | Description                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| `-c`, `--cached`   | Show all files currently tracked in the index (default behavior if no flag)                     |
| `-d`, `--deleted`  | Show files that have been deleted from the working directory but are still tracked in the index |
| `-m`, `--modified` | Show files that have been modified in the working directory but not yet staged                  |
| `-o`, `--others`   | Show untracked files — files in the working directory not listed in the index                   |
| `-s`, `--stage`    | Show staged entries with detailed mode, object hash, and stage number                           |

```bash
gitlite ls-files [options]
```

---

### 🧱 Command: `hash-object`

This command computes the SHA-1 hash of a file’s contents — simulating how Git creates **blob** objects.

By default, it only prints the hash. If the `-w` (write) flag is passed, it stores the object in `.gitlite/objects/`.

---

#### 🔧 Usage

| Option     | Description                                                    |
| ---------- | -------------------------------------------------------------- |
| `-w`       | Writes the corresponding blob object into `.gitlite/objects/.` |

```bash
gitlite hash-object <file>
```
Prints the SHA-1 hash of the file content.
```bash
gitlite hash-object -w <file>
```
Prints the SHA-1 hash and writes the corresponding blob object into `.gitlite/objects/.`

*Note: GitLite is a minimal Git implementation focused on essential features. If a feature doesn’t add significant value, it’s intentionally left out to keep the project simple and focused. For example, support for the -t option with tree and commit types was deemed unnecessary and not implemented.

---

### 🧱 Command: `write-tree`

The `write-tree` command creates a tree object from the current state of the index (staging area). It writes all the tracked files and directories into a tree object and returns the SHA-1 hash of that tree.

---

#### 🔧 Usage

| Option     | Description                                                    |
| ---------- | -------------------------------------------------------------- |
| `--prefix` | Writes a subtree starting at the specified directory prefix    |

```bash
gitlite write-tree [--prefix=<prefix>]
```
By default, it writes the tree object representing the entire index.

The optional --prefix argument allows writing a subtree starting at the specified directory prefix.

---

### 🧱 Command: `cat-file`

The `cat-file` command displays information about GitLite repository objects by their SHA-1 hash.

---

#### 🔧 Usage

```bash
gitlite cat-file <type> <object>
gitlite cat-file [-s | -p | -t] <object>
```
<type>: The type of object to inspect (e.g., blob, tree, commit).

-s : Show the size of the object in bytes.

-p : Pretty-print the contents of the object.

-t : Show the type of the object.

*⚠️ <object> is the SHA-1 hash

---

## 🧾 Next Features / To Do List

Below is a checklist of implemented and planned features for GitLite, along with short descriptions of their purpose:

### ✅ Completed

- [x] `init` – Initialize a new GitLite repository with `.gitlite` structure and local configuration
- [x] `add` – Stage files by updating the index with changes from the working directory
- [x] `commit` – Create a snapshot of the staged changes as a new commit object
- [x] `ls-files` – Display the contents of the index with filtering options (cached, modified, deleted, etc.)
- [x] `hash-object` – Compute and optionally store the SHA-1 hash of a file’s contents as a blob object
- [x] `write-tree` – Write a tree object representing the current state of the index
- [x] `cat-file` – Inspect stored GitLite objects (blob, tree, commit) by type, content, or size
- [x] `status` – Show the state of the working directory and staging area (staged, modified, untracked, deleted)

### 🛠️ In Progress / Planned

- [ ] `rm` – Remove files from both the working directory and index
- [ ] `restore` – Restore files from the index or a specific commit to the working directory
- [ ] Refactor internal code – Restructure modules for better readability, maintainability, and extensibility
- [ ] Keep testing the program – Add unit tests and test real-world workflows to ensure stability and correctness

> ✅ GitLite is being built with learning in mind — some Git features are intentionally simplified to focus on clarity and understanding.

---

## 🤝 Contributing

Contributions are very welcome!

If you find any bugs or have ideas for improvements, feel free to contact me through this email:

```
raulcortes.dev@gmail.com
```
