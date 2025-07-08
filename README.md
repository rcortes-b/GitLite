# GitLite

**GitLite** is a minimal Git implementation built from scratch in Python to explore and understand the inner workings of Git version control.

---

## Table of Contents

- [🎯 Purpose](#-purpose)
- [📚 References & Inspiration](#-references--inspiration)
- [🛠️ Installation](#-installation)
- [🚀 Usage](#-usage)
- [🧾 Commands](#commands)
  - [🧱 Command: `init`](-command-init)
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
Creates a .gitlite/ folder in the current directory.
```bash
gitlite init <name>
```
Creates a new folder named <name> and initializes .gitlite/ inside it.
```bash
gitlite init my_repo --author=rcortes- --email=randomemail@email.com
```
All in one init usage
