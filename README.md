# Kor
`💣BOOM BUILDING CORPORATION 💣` Custom Discord Bot.

## Index
- [Kor](#kor)
  - [Index](#index)
  - [Description](#description)
  - [Main Features](#main-features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)

## Description
`Kor` is a Discord bot created for [💣BOOM BUILDING CORPORATION 💣](https://discord.com/invite/boombuilding).  
This bot is specifically designed for the `💣BOOM BUILDING CORPORATION 💣` server.

## Main Features
- **Welcome new members:** Gives a warm welcome to new users.  
- **Daily facts:** Learn something new every day.  
- **Ticket system:** Get support in the easiest way possible.  

## Getting Started

### Prerequisites
- Python 3.8 or a higher version is required (this bot has been tested on `Python 3.11.6` and `Python 3.10`).  
  - Download and install Python [here](https://www.python.org/downloads/).  
- [Pip](https://pip.pypa.io/en/stable/) (Python package manager).  

### Installation
1. Clone the repository (requires [Git](https://git-scm.com/)):  
   ```sh
   git clone https://github.com/Stageddat/kor.git
   ```

2. Install dependencies using [pip](https://pip.pypa.io/en/stable/):  
   ```sh
   pip3 install -r requirements.txt
   ```

3. Create a `.env` file and insert the tokens:  
   ```bash
   TOKEN=DISCORD_BOT_TOKEN
   GITHUB_TOKEN=GITHUB_PAT_TOKEN
   PRIVATE_API=PRIVATE_API_URL
   PRIVATE_API_KEY_TOKEN=PRIVATE_API_URL_TOKEN
   ```

4. Edit the variables in `config.py` and `src/global_src`.  

5. Install and set up the API. Resources can be found in the `api` folder.  

6. Run the bot:  
   ```sh
   py main.py
   ```