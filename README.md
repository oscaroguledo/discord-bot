# **Discord Bot with Invite Link Tracking and Role Assignment**

## **Overview**

This project is a Discord bot written in Python using the `discord.py` library. The bot tracks when members join a server through a specific invite link and automatically assigns a role to the member who joins. It also provides functionalities for managing the bot (e.g., shutting it down) and logs server activities, such as when members join or leave the server.

## **Features**

1. **Invite Link Tracking**:
    - The bot tracks which invite link was used to join the server.
    - Logs details about the invite and the inviter.
   
2. **Role Assignment**:
    - Automatically assigns a specific role to a new member upon joining the server through an invite link.
   
3. **Bot Commands**:
    - `shutdown`: Allows the owner of the bot to safely shut down the bot.

4. **Event Handlers**:
    - Handles events for members joining and leaving the server.
    - Sends welcome and goodbye messages when members join or leave the server.

## **Dependencies**

Before running this project, make sure you have the following dependencies installed:

1. **Python 3.8+**
2. **discord.py (Discord API Wrapper)**:
   ```bash
   pip install discord.py
   ```
3. **requests** (For sending HTTP requests):
   ```bash
   pip install requests
   ```

## **Bot Setup**

### **Bot Token**
- The bot requires a **token** to connect to the Discord API. This token is provided by Discord when you create a new bot via the [Discord Developer Portal](https://discord.com/developers/applications).
- **Note**: Never expose your token publicly, as it grants full control over your bot. In this project, the token is stored as a string in the script, but it is recommended to load it from a secure file or environment variable for production.

### **Roles and Permissions**
- The bot requires the `Manage Roles` permission to assign roles to members.
- You must provide a valid `role_id` for the bot to assign that role to new members.

### **Invite Links**
- The bot tracks the invite link used to join the server and logs details about the member who joined and the inviter.

### **Guild/Server ID**
- The bot requires the server's (guild's) ID where it's active. This ID should be passed as the `guild_id` in the script.

### **Role ID**
- The bot assigns a specific role to new members based on the `role_id` provided.

### **Owners**
- The bot includes an owner validation system. It accepts a list of owner IDs, which grants certain privileges (like shutting down the bot). Only the IDs listed in `OWNERS_IDS` can access these privileges.

## **Project Structure**

```plaintext
discord_bot_project/
│
├── bot.py             # Main script for running the bot
├── README.md          # Documentation
├── token.txt          # (Optional) Store your token here (for secure access)
```

## **Code Explanation**

### **Main Functionality**

The bot's core functions include:

1. **Invite Link Handling**:
   - The bot tracks invite links using the `guild.invites()` method.
   - When a member joins the server, it compares the number of uses for each invite to determine which invite was used.

2. **Assigning Roles**:
   - When a user joins the server, the bot sends a `PUT` request to Discord's API to assign the specified role to the user using the `assign_guild_role()` function.
   
   ```python
   def assign_guild_role(guildid, token, role_id, user_id):
       headers = {'Content-Type': 'application/json', 'authorization': f'Bot {token}'}
       url = f"https://discord.com/api/v9/guilds/{guildid}/members/{user_id}/roles/{role_id}"
       response = requests.request("PUT", url=url, headers=headers)
       # Handling response...
   ```

3. **Event Handling**:
   - The bot listens for events such as `on_ready()`, `on_member_join()`, and `on_member_remove()`.
   - When a member joins, it checks the invite link and assigns the role.
   - When a member leaves, it logs the action.

### **Key Events and Commands**

- **on_ready()**:
   Triggered when the bot connects to the Discord server and is ready to function.
   
- **on_member_join()**:
   Handles new member joins, checks which invite link was used, and assigns the role.

- **on_member_remove()**:
   Logs when a member leaves the server.

- **shutdown**:
   Command to safely shut down the bot, only accessible by the bot owner.

## **How to Run the Bot**

1. **Clone or Download the Repository**:
   Clone this project from GitHub or download the repository to your local machine.

2. **Install Dependencies**:
   Install the necessary dependencies listed above.

3. **Update Configuration**:
   - Replace the placeholder values in the script with actual values for:
     - `token`: Your Discord bot token.
     - `guild_id`: The ID of your server.
     - `role_id`: The ID of the role to be assigned.
     - `OWNERS_IDS`: List of owner user IDs.

4. **Run the Bot**:
   After everything is set up, run the bot by executing the script:

   ```bash
   python bot.py
   ```

   The bot will connect to your server, start tracking invites, and assign roles to new members.

## **Security Considerations**

- **Token Management**: It’s critical to ensure the bot token is kept secure. It should ideally be stored in a secure file or environment variable rather than hardcoded in the script.
  
- **Permissions**: Ensure the bot has the necessary permissions in the Discord server (such as managing roles and reading messages).

- **APIs**: The bot makes API requests to Discord, so handling these requests and responses efficiently is crucial, especially with proper error handling.

## **Future Enhancements**

1. **Dynamic Role Assignment**: Allow for dynamic assignment of different roles based on the invite link used.
2. **Database Integration**: Store invite link usage statistics and member join data in a database for more detailed tracking.
3. **Logging Enhancements**: Implement a logging system to monitor bot activity and errors.
4. **Web Interface**: Provide a web dashboard to track invite usage and manage roles.

---

This bot provides a great foundation for automating Discord server management, especially for servers that want to keep track of invite links and assign specific roles to users who join using those links.
