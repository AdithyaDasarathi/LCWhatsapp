# 🤖 LeetCode WhatsApp Agent

An automated agent that sends you one easy, medium, and hard LeetCode problem daily via WhatsApp using the Twilio API.

## ✨ Features

- 📱 **WhatsApp Integration**: Sends problems directly to your WhatsApp
- 🎯 **Daily Problems**: One problem each of Easy, Medium, and Hard difficulty
- 🗄️ **Smart Tracking**: Never sends the same problem twice
- ⏰ **Scheduled Delivery**: Customizable daily send time
- 📊 **Statistics**: Track your progress and remaining problems
- 🔧 **Easy Setup**: Simple configuration with environment variables

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **Twilio Account** with WhatsApp API access
3. **WhatsApp Business Account** (for receiving messages)

## 🚀 Quick Setup

### 1. Clone and Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Set Up Twilio WhatsApp

1. **Create a Twilio Account**: Go to [Twilio Console](https://console.twilio.com/)
2. **Get WhatsApp Sandbox**: Navigate to Messaging → Try it out → Send a WhatsApp message
3. **Join Sandbox**: Send the sandbox join code from your WhatsApp to the Twilio number
4. **Get Credentials**: Note your Account SID and Auth Token from the console

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
# Twilio WhatsApp API Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890

# Scheduling Configuration (24-hour format)
DAILY_SEND_TIME=09:00
TIMEZONE=America/New_York

# Database Configuration (optional)
DATABASE_PATH=leetcode_agent.db
```

**Important**: Replace the phone numbers and credentials with your actual values!

### 4. Test the Setup

```bash
# Test all components
python leetcode_agent.py --test
```

This will:
- ✅ Test WhatsApp connection
- ✅ Fetch LeetCode problems
- ✅ Verify database functionality

## 🎮 Usage

### Start the Daily Agent

```bash
# Start the scheduled agent (runs continuously)
python leetcode_agent.py
```

The agent will run continuously and send problems at your configured time daily.

### Manual Commands

```bash
# Send problems immediately (once)
python leetcode_agent.py --once

# Send problem statistics
python leetcode_agent.py --stats

# Fetch all LeetCode problems manually
python leetcode_agent.py --fetch

# Test the complete setup
python leetcode_agent.py --test
```

## 📱 Sample WhatsApp Message

```
🚀 Daily LeetCode Challenge! 🚀

Here are your 3 problems for today:

🟢 EASY: Two Sum
🔗 https://leetcode.com/problems/two-sum/

🟡 MEDIUM: Add Two Numbers
🔗 https://leetcode.com/problems/add-two-numbers/

🔴 HARD: Median of Two Sorted Arrays
🔗 https://leetcode.com/problems/median-of-two-sorted-arrays/

Good luck and happy coding! 💪

Remember:
• Read the problem carefully
• Think about edge cases
• Optimize your solution
• Test with examples
```

## ⚙️ Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | Required |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | Required |
| `TWILIO_WHATSAPP_FROM` | Twilio WhatsApp number | `whatsapp:+14155238886` |
| `YOUR_WHATSAPP_NUMBER` | Your WhatsApp number | Required |
| `DAILY_SEND_TIME` | Time to send (HH:MM) | `09:00` |
| `TIMEZONE` | Your timezone | `America/New_York` |
| `DATABASE_PATH` | SQLite database path | `leetcode_agent.db` |

## 🗄️ Database Schema

The agent uses SQLite to track problems and prevent duplicates:

- **problems**: Stores all LeetCode problems
- **sent_problems**: Tracks which problems were sent when
- **daily_batches**: Records complete daily sends

## 🔧 Troubleshooting

### WhatsApp Issues

**Problem**: "WhatsApp not configured" error
- **Solution**: Check your `.env` file and ensure all Twilio credentials are correct

**Problem**: Messages not being delivered
- **Solution**: 
  1. Verify you've joined the Twilio WhatsApp sandbox
  2. Check your phone number format (include country code)
  3. Ensure your Twilio account has WhatsApp enabled

### LeetCode Issues

**Problem**: "No problems found" error
- **Solution**: Run `python leetcode_agent.py --fetch` to manually fetch problems

**Problem**: "Missing problems for difficulties" error
- **Solution**: The agent has run out of unsent problems. This happens after ~2000+ days of use!

### General Issues

**Problem**: Agent stops running
- **Solution**: Use a process manager like `systemd`, `pm2`, or run in a `screen` session

**Problem**: Timezone issues
- **Solution**: Check your timezone setting. Use format like `America/New_York`, `Europe/London`, etc.

## 🚀 Running in Production

### Option 1: Screen Session (Simple)
```bash
# Start in a detached screen session
screen -S leetcode-agent
python leetcode_agent.py
# Press Ctrl+A, then D to detach
```

### Option 2: Systemd Service (Linux)
Create `/etc/systemd/system/leetcode-agent.service`:

```ini
[Unit]
Description=LeetCode WhatsApp Agent
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/agent
ExecStart=/usr/bin/python3 leetcode_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable leetcode-agent
sudo systemctl start leetcode-agent
```

## 📊 Statistics

The agent tracks:
- Total problems by difficulty
- Problems sent so far
- Remaining problems
- Daily send history

View stats: `python leetcode_agent.py --stats`

## 🔒 Security Notes

- Keep your `.env` file secure and never commit it to version control
- Your Twilio credentials have access to send messages - protect them
- The agent only fetches free LeetCode problems (no premium required)

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the agent!

## 📄 License

MIT License - feel free to use and modify as needed.

---

**Happy Coding! 🚀**

Made with ❤️ for the coding community #   L C W h a t s a p p  
 