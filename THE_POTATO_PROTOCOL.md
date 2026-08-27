# 🥔 THE POTATO PROTOCOL

**The no-experience-required guide to running Offline 2FA.**

If you've never opened a terminal in your life and the word "Python" makes you nervous, you're in exactly the right place. Follow these steps in order. Don't skip. You'll be fine.

---

## Step 0 — Do you even need to do any of this?

If someone handed you a file called **`Offline2FA.exe`**, congratulations, you're done before you started. Double-click it. That's the entire process. Close this guide and go live your life.

Everyone else, keep reading. 🥔

---

## Step 1 — Get Python

Offline 2FA runs on Python 3.13. Let's get it.

1. Go to **https://www.python.org/downloads/**
2. Download Python **3.13** (the big yellow button usually has the latest version).
3. Run the installer.
4. **VERY IMPORTANT:** on the first screen, tick the box that says **"Add Python to PATH"** before you click Install. This one checkbox saves you a world of pain. Tick it. 🥔
5. Click Install. Wait. Done.

## Step 2 — Get the Offline 2FA files

If you downloaded a ZIP of the project, right-click it and choose **Extract All**. Remember where you put the folder — say, your Desktop.

Inside that folder you should see a file called `main.py`. Good. That's home base.

## Step 3 — Open a terminal *in that folder*

This sounds scary. It is not.

- **Windows:** open the Offline2FA folder, click the address bar at the top, type `cmd`, and press Enter. A black window appears. That's the terminal. It's already sitting in the right folder.
- **Mac:** open the Terminal app, type `cd ` (with a space after it), then drag the Offline2FA folder onto the terminal window and press Enter.

## Step 4 — Install the bits Offline 2FA needs

In that terminal window, type this exactly and press Enter:

```
pip install -r requirements.txt
```

A bunch of text will scroll by. That's normal — it's downloading the pieces. Wait until it stops and gives you back a fresh line to type on. ☕ (Grab a coffee, first time can take a minute.)

> Stuck? If `pip` isn't recognized, you probably missed the "Add Python to PATH" checkbox in Step 1. Reinstall Python and tick it this time. 🥔

## Step 5 — Run it

Same terminal, type this and press Enter:

```
python main.py
```

The Offline 2FA window pops open. **You did it.** 🎉

## Step 6 — Actually using it

1. Click **+ Add**.
2. Paste your 2FA secret key (or the `otpauth://` link, or import a QR image).
3. Optionally give it a name so you know which is which.
4. Click **Add**.

Your code shows up and refreshes itself every 30 seconds. Click the card to copy the code. That's the whole app.

---

## Next time you want to run it

You don't repeat all of this. Just do **Step 3** (open a terminal in the folder) and **Step 5** (`python main.py`). Two steps forever after.

## Want the one-file version for yourself?

Once it's running, you can build your own `Offline2FA.exe` — a single file you can copy to any Windows PC with nothing installed. In the terminal:

```
pyinstaller Offline2FA.spec
```

When it finishes, look inside the new **`dist`** folder. Your `Offline2FA.exe` is in there. Copy it anywhere. Double-click. No Python needed on that machine at all.

---

*You are now a certified Offline 2FA operator. Full potato clearance granted.* 🥔✅
