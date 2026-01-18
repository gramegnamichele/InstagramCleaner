# ✨ InstagramCleaner - Instagram Non-Mutual Finder

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>Find out who doesn't follow you back on Instagram</b>
</p>

---

## 🎯 What is InstagramCleaner?

InstagramCleaner is a modern desktop application that analyzes your Instagram data export to find users who don't follow you back. With a sleek dark-themed UI and smooth animations, it makes cleaning up your Instagram following list a breeze.

## ✨ Features

- 🎨 **Modern Dark UI** - Beautiful interface built with CustomTkinter
- 📊 **Animated Statistics** - See your followers, following, and non-mutual counts with counting animations
- 🔗 **Clickable Profiles** - Click on any username to open their Instagram profile directly
- 📋 **Export Results** - Save the list to a TXT file
- 📎 **Copy to Clipboard** - Quickly copy all usernames
- ⚡ **Fast Analysis** - Processes thousands of users in seconds
- 🌙 **Fade-in Animation** - Smooth startup experience

## 📸 Screenshots

![InstagramCleaner Interface](https://via.placeholder.com/800x500/0f0f1a/6366f1?text=InstagramCleaner+Interface)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gramegnamichele/InstagramCleaner.git
   cd InstagramCleaner
   ```

2. **Install dependencies**
   ```bash
   pip install customtkinter
   ```

3. **Run the application**
   ```bash
   python InstagramCleaner.py
   ```

## 📥 How to Get Your Instagram Data

1. Open **Instagram** and go to **Settings**
2. Navigate to **Accounts Center** (Centro gestione account)
3. Click on **Your information and permissions** (Le tue informazioni e autorizzazioni)
4. Select **Download your information** (Esporta le tue informazioni)
5. Click **Create export** (Crea esportazione)
6. Choose **Export to device** (Esporta sul dispositivo)
7. Set **Format** to **JSON**
8. Set **Date range** to **All time** (Sempre)
9. Click **Customize information** (Personalizza informazioni)
10. Select **only** these two options:
    - ✅ **Followers**
    - ✅ **Following** (Persone/Pagine seguite)
11. Click **Start export** (Avvia esportazione)
12. Wait for Instagram to prepare your data (you'll receive a notification)
13. Download and extract the ZIP file
14. You'll find these files in the `followers_and_following` folder:
    - `followers_1.json`
    - `following.json`

## 🎮 How to Use

1. Launch **InstagramCleaner**
2. Click **Browse** to select your `followers_1.json` file
3. Click **Browse** to select your `following.json` file
4. Click **🔍 Analyze Now**
5. View the list of users who don't follow you back
6. Click on any user to open their Instagram profile
7. Use **Export to TXT** or **Copy All** to save the results

## 🛠️ Built With

- [Python](https://www.python.org/) - Programming language
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI library

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<p align="center">
  <b>Michele Gramegna</b>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/michele-gramegna-61a0773a6/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://github.com/gramegnamichele">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

---

<p align="center">
  Made with 💜 for Instagram cleanup
</p>
