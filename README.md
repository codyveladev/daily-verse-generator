# Daily Verse 🌿

**A simple, beautiful web app that delivers a personalized Bible verse every day — based on what you're going through.**

No ads. No noise. Just Scripture, chosen thoughtfully for your heart.

![Daily Verse Preview](https://via.placeholder.com/1200x630/667eea/ffffff?text=Daily+Verse+-+Personalized+Daily+Scripture)  
*(Clean dashboard with today's verse and your history)*

## ✨ Features

- **Personalized Daily Verse** – Set your current mood (grief, anxiety, joy, peace, etc.) and get a relevant Bible verse chosen by Google Gemini AI.
- **Intelligent Verse Selection** – AI picks the most comforting and encouraging verse for how you're feeling.
- **Accurate Scripture** – Full verse text pulled from [bible-api.com](https://bible-api.com)
- **Verse History** – View your last 10 previous verses with date and mood context.
- **Modern, Calming UI** – Built with Bootstrap 5 — fully responsive and peaceful design.
- **Secure & Private** – Register, log in, update profile — your data stays yours.
- **Instant Test Data** – One script gives you 30 days of history for demo purposes.

## 🚀 Quick Start (Fixed & Working Setup)

### Prerequisites
- Python 3.9 or higher
- A free [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Step-by-Step Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/daily-verse.git
cd daily-verse

# 2. Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt