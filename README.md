## https://github.com/Codemaster-AR/texty-bird

---

# 🐦 texty_bird

A retro, terminal-based Flappy Bird clone written in Python.

---

## 🐍 1. Install Python 3

Before playing, you must have **Python 3** installed.

* **Download:** Visit [python.org/downloads](https://www.python.org/downloads/).
* **Setup:** Follow the installer instructions.
* **Important for Windows:** Ensure you check the box **"Add Python to PATH"** during installation.

---

## 📂 2. Set Up Your Folders

To get the game running, you need to create a specific folder structure on your **Desktop**:

1. **Create Folders:** Create a folder on your Desktop named `Texty_bird`. Inside that folder, create another folder named `texty-bird`.
2. **Open Terminal:** Open your terminal (Mac/Linux) or Command Prompt (Windows).
3. **Navigate:** Use the following command to enter your new folder:

```bash
cd Desktop/Texty_bird/texty-bird

```

4. **Clone the Game:** Run this command to download the files into that folder:

```bash
git clone https://github.com/Codemaster-AR/texty-bird.git .

```

---

## 🐧 For Mac & Linux Users

You have **two options** to play the game:

### Option A: The Simple Way

1. Navigate to your `texty-bird` folder on the Desktop.
2. Find the file labeled as the **Unix executable**.
3. **Double-click** it to start the game instantly.

### Option B: Using the Terminal

1. Install the required library:
```bash
pip3 install curses

```


2. Run the game using Python 3:
```bash
python3 texty_bird.py

```



---

## 🪟 For Windows Users

1. **Install Requirements:**
Windows requires a specific library to run the game's interface. Open Command Prompt and run:
```bash
pip install windows-curses

```


2. **Run the Game:**
Start the game with the following command:
```bash
python3 texty_bird.py

```



---

Would you like me to explain how to fix the "Command not found" error if the terminal doesn't recognize `python3`?
