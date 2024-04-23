# Kor
`💣BOOM BUILDING CORPORATION 💣` custom Discord Bot.

## Index
1. [Description](#description)
2. [Main features](#main-features)
3. [For start](#for-start)
    1. [Pre requisites](#prerequisites)
    2. [Installation](#installation)

## Description
`Kor` is a Discord bot for [💣BOOM BUILDING CORPORATION 💣](https://discord.com/invite/boombuilding).<br>
This is bot is specific and only for `💣BOOM BUILDING CORPORATION 💣` server.

## Main features
- **Welcome new members:** Gives a warm welcome to new users.
- **Daily facts:** Learn something new every day.
- **Ticket system:** Get support with the most easy way.

## For start

### Prerequisites
- Need python 3.8 or higher version (This bot tested in `Python 3.11.6` and `Python 3.10`). 
  - Get and install python [here](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/)

### Installation
1. Clone the repository (requires [git](https://git-scm.com/)):
```sh
git clone https://github.com/Stageddat/kor.git
```

2. Install dependencies using [pip](https://pip.pypa.io/en/stable/) (a Python package manager):
```sh
$ pip3 install -r requirements.txt
```
3. Create a file with `.env` name and insert the tokens:
```bash
TOKEN = DISCORD_BOT_TOKEN
GITHUB_TOKEN = GITHUB_PAT_TOKEN
PRIVATE_API = PRIVATE_API_URL
PRIVATE_API_KEY_TOKEN = PRIVATE_API_URL_TOKEN
```
4. Edit the variables of `config.py` and `src/global_src`.
5. Install and setup API, you can find the resources in the `api` folder.
6. Run:
```sh
py main.py
```