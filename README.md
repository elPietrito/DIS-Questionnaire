# Audio Survey Application - Streamlit Version

A two-part survey application for audio perception experiments.

## 📁 Project Structure

```
streamlit_survey/
├── app.py                    # Main entry point
├── config.py                 # EDIT QUESTIONS HERE
├── state_manager.py          # Session state management
├── experimenter_page.py      # Part 1 interface
├── participant_page.py       # Part 2 interface
├── csv_handler.py           # CSV generation
├── requirements.txt         # Python dependencies
└── participants/            # Auto-created data folder
    └── {participant_id}/
        ├── audio_files/     # Uploaded audio files
        └── responses.csv    # Survey responses
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Customize Your Questions

**Edit `config.py`** to change:
- Question text (look for clear comments like `# ← Edit question text here`)
- Number of questions (add/remove lines in the question lists)
- Likert scale range (LIKERT_MIN, LIKERT_MAX)
- Maximum episodes (MAX_EPISODES)
- CSV column labels

### 3. Run the Application

```bash
streamlit run app.py
```

## Usage for Phone Hotspot Setup

### Step 1: Set Up Hotspot
1. Enable mobile hotspot on your phone
2. Connect your computer to the phone's hotspot
3. Connect the tablet to the same hotspot

### Step 2: Run the Server
1. On your computer, run: `streamlit run app.py`
2. Streamlit will show URLs like:
   ```
   Network URL: http://192.168.X.X:8501
   ```
3. Note down this Network URL

### Step 3: Experimenter Workflow (Part 1)
1. On your computer, open the app (it opens automatically)
2. Enter participant ID (e.g., "P001")
3. For each episode:
   - Upload audio file 1
   - Fill Likert scale and dropdown for audio 1
   - Upload audio file 2
   - Fill Likert scale and dropdown for audio 2
4. Use navigation buttons:
   - **Previous/Next**: Navigate between episodes
   - **Add Episode**: Create new episode (up to 5 total)
   - **Delete**: Remove current episode
5. Click "Generate Participant Link" when ready

### Step 4: Participant Workflow (Part 2)
1. Copy the participant link shown on screen
2. Open it on the tablet browser
3. Participant will:
   - Listen to each audio
   - Type what they heard
   - Answer Likert questions
   - Navigate through all episodes
4. Click "Finish Survey" to save data

### Step 5: Find Your Data
CSV files are saved in:
- `participants/{participant_id}/responses.csv` (individual)
- `all_participants_data.csv` (all participants combined)

## 🎯 Key Features

✅ **Experimenter can:**
- Add, edit, and delete episodes
- Preview uploaded audio files
- See progress at each step
- Generate shareable participant link

✅ **Participant can:**
- Listen to audio files in browser
- Navigate between episodes
- View progress indicator
- Complete survey and save data

✅ **Data Management:**
- Automatic folder creation
- Individual + global CSV files
- Preserves original audio filenames
- Easy-to-analyze format

## 📝 Customization Guide

### To Change Questions:

1. Open `config.py`
2. Find the section you want to edit:

```python
# For Audio 1 questions (Part 2):
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Audio 1 – Likert question 1",  # ← Change this text
    "Audio 1 – Likert question 2",  # ← Change this text
    # Add more by copying a line above
]
```

### To Add Questions:

Just copy a line and add it:

```python
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Audio 1 – Likert question 1",
    "Audio 1 – Likert question 2",
    "Audio 1 – Likert question 3",  # ← New question
]
```

### To Change Likert Scale:

```python
LIKERT_MIN = 1  # Change minimum value
LIKERT_MAX = 7  # Change maximum value (e.g., 1-7 scale)
```

## 🔧 Troubleshooting

**Problem:** Participant can't access the link
- **Solution:** Make sure both devices are on the same WiFi/hotspot

**Problem:** Audio files not playing
- **Solution:** Use .wav, .mp3, or .ogg formats

**Problem:** CSV not saving
- **Solution:** Check that `participants/` folder has write permissions

## 📊 CSV Output Format

Each row contains:
- Participant ID
- For each episode:
  - Part 1: audio paths, likert scores, choices
  - Part 2: text responses, likert answers

Headers are auto-generated from your questions in `config.py`.

## 🆘 Support

If you need to modify anything:
1. Check `config.py` first (most settings are there)
2. Look for comments starting with `# ←` for edit locations
3. Each file has a header explaining its purpose
