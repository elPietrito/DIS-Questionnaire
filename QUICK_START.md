# 🚀 QUICK START GUIDE

## Installation (5 minutes)

1. **Install Streamlit:**
   ```bash
   pip install streamlit
   ```

2. **Put all files in one folder:**
   - app.py
   - config.py
   - state_manager.py
   - experimenter_page.py
   - participant_page.py
   - csv_handler.py

## Running the Application

### For Phone Hotspot Setup:

1. **Turn on phone hotspot** and connect both computer and tablet to it

2. **On your computer, run:**
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **You'll see output like:**
   ```
   Network URL: http://192.168.43.100:8501
   ```

4. **Write down this Network URL** - you'll share it with participants!

## Workflow

### Part 1 - Experimenter (on computer):
1. Enter participant ID
2. Upload audio files (one or two per episode)
3. Fill in Likert scales and dropdowns
4. Click "Add Episode" to create more (up to 5)
5. Click "Generate Participant Link" when done
6. **Share the link with participant**

### Part 2 - Participant (on tablet):
1. Open the link from experimenter
2. Listen to audio files
3. Type what you heard
4. Answer Likert questions
5. Click "Next" or "Finish" at the end

## Data Location

Your data will be saved in:
- `participants/P001/responses.csv` (individual participant)
- `all_participants_data.csv` (all participants combined)

## Customizing Questions

**Open `config.py` and look for these sections:**

```python
# Change Audio 1 questions here:
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Your question 1",  # ← Edit this
    "Your question 2",  # ← Edit this
]

# Change Audio 2 questions here:
PART2_AUDIO2_LIKERT_QUESTIONS = [
    "Your question 1",  # ← Edit this
    "Your question 2",  # ← Edit this
]
```

To add more questions, just copy a line and add it!

## Tips

✅ Make sure audio files are .wav, .mp3, or .ogg format
✅ Both devices must be on the same WiFi/hotspot
✅ You can edit episodes before generating the participant link
✅ Data is saved automatically when participant clicks "Finish"

## Need Help?

- Check that both devices show the same WiFi name
- Try using the Network URL (not localhost)
- Make sure files are in the same folder
- Check `config.py` for question settings
