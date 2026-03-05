# 📚 CODE STRUCTURE EXPLANATION

## Overview

This application has **6 Python files** that work together:

```
┌─────────────────────────────────────────────────┐
│                    app.py                       │
│              (Main Entry Point)                 │
│  • Starts the application                       │
│  • Checks URL for ?participant=ID               │
│  • Routes to correct interface                  │
└────────────┬───────────────────────┬────────────┘
             │                       │
             ▼                       ▼
   ┌──────────────────┐    ┌──────────────────┐
   │ experimenter_    │    │  participant_    │
   │    page.py       │    │     page.py      │
   │                  │    │                  │
   │ (Part 1)         │    │ (Part 2)         │
   │ • Upload audio   │    │ • Listen audio   │
   │ • Fill forms     │    │ • Write text     │
   │ • Add episodes   │    │ • Answer Qs      │
   └─────┬────────────┘    └────────┬─────────┘
         │                          │
         │    ┌──────────────────┐  │
         └───►│ state_manager.py │◄─┘
              │                  │
              │ • Stores data    │
              │ • Manages nav    │
              │ • Creates empty  │
              │   episodes       │
              └────────┬─────────┘
                       │
              ┌────────▼─────────┐
              │  csv_handler.py  │
              │                  │
              │ • Creates CSV    │
              │ • Saves data     │
              └────────┬─────────┘
                       │
              ┌────────▼─────────┐
              │    config.py     │
              │                  │
              │   EDIT THIS!     │
              │ • Questions      │
              │ • Settings       │
              │ • Labels         │
              └──────────────────┘
```

## File Responsibilities

### 1. **app.py** - The Traffic Controller
- **What it does:** Decides which page to show
- **When to edit:** Almost never (unless changing page layout)
- **Key code:**
  ```python
  if participant_id:
      render_participant_page()  # Show Part 2
  else:
      render_experimenter_page()  # Show Part 1
  ```

### 2. **config.py** - The Settings File 
- **What it does:** Stores all questions, labels, and settings
- **When to edit:** Every time you want to change questions!
- **What you can change:**
  - Question text
  - Number of questions (add/remove lines)
  - Likert scale range (1-6, 1-7, etc.)
  - Dropdown options
  - CSV column names
  - File paths

### 3. **state_manager.py** - The Memory Keeper
- **What it does:** Remembers data as user navigates
- **When to edit:** Rarely (structure is good as-is)
- **Key functions:**
  - `create_empty_episode()` - Makes blank episode
  - `add_new_episode()` - Adds episode to list
  - `delete_episode()` - Removes episode
  - `get_active_episodes()` - Gets filled episodes

### 4. **experimenter_page.py** - Part 1 Interface
- **What it does:** Shows upload and form interface
- **When to edit:** If you want to change layout/design
- **Key sections:**
  - Participant ID input
  - Audio file uploaders
  - Likert scales
  - Dropdown menus
  - Navigation buttons
  - Link generator

### 5. **participant_page.py** - Part 2 Interface
- **What it does:** Shows audio player and questions
- **When to edit:** If you want to change layout/design
- **Key sections:**
  - Progress bar
  - Audio players
  - Text input boxes
  - Likert questions
  - Navigation buttons

### 6. **csv_handler.py** - The Data Saver
- **What it does:** Creates CSV files from data
- **When to edit:** If you want different CSV format
- **Key functions:**
  - `generate_csv_header()` - Makes column names
  - `flatten_episodes_to_row()` - Turns data into row
  - `save_all_data()` - Writes CSV files

## Data Flow Example

Let's trace what happens when experimenter uploads an audio file:

```
1. Experimenter clicks "Upload Audio 1"
   │
   ├─► experimenter_page.py receives file
   │
2. File is saved to disk
   │   save_uploaded_audio() function
   │   → participants/P001/audio_files/episode1_audio1.wav
   │
3. Path is stored in session state
   │   state_manager.py
   │   → current_episode['audio1_path'] = "/path/to/file.wav"
   │
4. Audio player shows file
   │   st.audio(current_episode['audio1_path'])
   │
5. Participant opens link
   │   participant_page.py loads same path
   │
6. Participant listens and answers
   │   Answers stored in session state
   │
7. Participant clicks "Finish"
   │
   ├─► csv_handler.py called
   │
8. Data converted to CSV row
   │   flatten_episodes_to_row()
   │
9. CSV files written
   └─► participants/P001/responses.csv
       all_participants_data.csv
```

## Session State Structure

Here's what gets stored in memory while app is running:

```python
st.session_state = {
    'participant_id': 'P001',
    'current_episode_index': 0,
    'episodes': [
        {
            'audio1_path': '/path/to/audio.wav',
            'audio1_filename': 'myaudio.wav',
            'likert1': 4,
            'choice1': 'PP',
            'audio2_path': '/path/to/audio2.wav',
            'audio2_filename': 'myaudio2.wav',
            'likert2': 5,
            'choice2': 'PS',
            'audio1_text_response': 'I heard...',
            'audio1_likert_answers': [3, 4],
            'audio2_text_response': 'I heard...',
            'audio2_likert_answers': [5, 2],
        },
        # ... more episodes ...
    ]
}
```

## Folder Structure Created at Runtime

```
your_project_folder/
├── app.py
├── config.py
├── state_manager.py
├── experimenter_page.py
├── participant_page.py
├── csv_handler.py
├── requirements.txt
├── README.md
│
└── participants/              ← Created automatically
    ├── P001/                  ← One folder per participant
    │   ├── audio_files/       ← Uploaded audio files
    │   │   ├── episode1_audio1.wav
    │   │   ├── episode1_audio2.wav
    │   │   ├── episode2_audio1.wav
    │   │   └── episode2_audio2.wav
    │   └── responses.csv      ← Participant's data
    │
    ├── P002/
    │   ├── audio_files/
    │   └── responses.csv
    │
    └── all_participants_data.csv  ← All participants combined
```

## Common Modifications

### To Add a Question:

**File to edit:** `config.py`

```python
# Before:
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Question 1",
    "Question 2",
]

# After:
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Question 1",
    "Question 2",
    "Question 3",  # ← Just add this line!
]
```

### To Change Likert Scale:

**File to edit:** `config.py`

```python
# Change from 1-6 to 1-7:
LIKERT_MIN = 1
LIKERT_MAX = 7  # ← Change this number
```

### To Add Dropdown Option:

**File to edit:** `config.py`

```python
# Before:
PART1_CHOICE_OPTIONS = ["PP", "PS"]

# After:
PART1_CHOICE_OPTIONS = ["PP", "PS", "PX"]  # ← Add option
```

## Need to Change Something Else?

1. **Questions/Labels** → Edit `config.py`
2. **Page Layout** → Edit `experimenter_page.py` or `participant_page.py`
3. **CSV Format** → Edit `csv_handler.py`
4. **Navigation Logic** → Edit `state_manager.py`
5. **Main Routing** → Edit `app.py`

All files have extensive comments to guide you!
