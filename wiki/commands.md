# Wiki Commands

<details>
<summary>Wiki Index</summary>

- [Home](home.md)
- [Commands](commands.md)
- Config
- Troubleshooting
  - Facts sync
- Protocol and guide
  - Facts
    - Adding facts
    - Adding facts from Trivia of Roblox [Island wiki website](https://robloxislands.fandom.com/wiki/Islands_Wiki)
    - Change current number
    - egg
  - Welcome
    - Test welcome message with specific user
</details>

## Wait a min...
The following wiki is separating the commands of different classes and sub-classes.
<br>You can use the index command to go to the one you like

### General
- `/reload_cog (cog=str)`<br>
    Reload a specific cog

- `/version`<br>
    View the version, location and ping of the bot.

- `/kill`<br>
    Turn off the bot

### Facts
- Facts public commands
  - `/fact random` - Get a random fact
      <details>
        <summary>Example</summary>
        <img src="wiki_src/fact_img/fact_random_1.png" alt="drawing" width="500"/><br>
        <img src="wiki_src/fact_img/fact_random_2.png" alt="drawing" width="500"/>
      </details>

  - `/fact dog` - Get a random dog fact
    <details>
      <summary>Example</summary>
      <img src="wiki_src/fact_img/fact_dog_1.png" alt="drawing" width="500"/><br>
      <img src="wiki_src/fact_img/fact_dog_2.png" alt="drawing" width="500"/>
    </details>


  - `/fact cat` - Get a random cat fact
    <details>
      <summary>Example</summary>
      <img src="wiki_src/fact_img/fact_cat_1.png" alt="drawing" width="500"/><br>
      <img src="wiki_src/fact_img/fact_cat_2.png" alt="drawing" width="500"/>
    </details>
  - `/fact island` - Get a random Roblox Island fact
    <details>
      <summary>Example</summary>
      <img src="wiki_src/fact_img/fact_island_1.png" alt="drawing" width="500"/><br>
      <img src="wiki_src/fact_img/fact_island_2.png" alt="drawing" width="500"/>
    </details>
- Facts admin commands
  - `/change_fact_number (number=int)`<br>
  Change the **next day faily fact number**
  - `/add_custom_island_fact (fact=str, img_link=Optional(str), source_link=Optional(str))`<br>
  Add a new Roblox Island custom fact
  - `/add_island_trivia (link=str)`<br>
  Extract facts from Roblox Island trivia
  - `/sync_island_fact_database`<br>
  Sync between Fact list MD and JSON database
  - `/sync_island_fact_github`<br>
  Sync the local and Github files

### Welcome System
- `/test_welcome (member=discord.Member)`<br>
    This will act like someone new joined but for the selected member
