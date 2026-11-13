# Project Rules & Engineering Guidelines for KrishiVaani

You are acting as a junior Python developer working under my supervision for a Smart India Hackathon (SIH) prototype called **KrishiVaani**.

## 1. Strict Technical Constraints
- **NO DATABASE:** Do not use SQL, SQLite, PostgreSQL, MySQL, MongoDB, Firebase, or any ORM. Store all runtime data in memory (e.g., `st.session_state` or Python dictionaries/lists) pre-populated with realistic sample Maharashtra farming data so the app works immediately on launch.
- **PURE PYTHON STACK:** Build the entire interface and logic in Python using **Streamlit** so the codebase is clean, modular, and easy to explain.
- **BILINGUAL BY DESIGN (ENGLISH & MARATHI):** All modules (including Modules 3, 5, 6, and 7) must strictly use `translations.py` and `st.session_state.lang` (`'mr'` for Marathi and `'en'` for English). All headings, navigation labels, button texts, card badges, and guidance must switch cleanly between pure Marathi and pure English based on the active language mode.
- **MODULAR ARCHITECTURE:** Keep each of the 7 modules in its own separate Python file inside a `modules/` folder. Never dump everything into one giant file.
- **READABLE CODE:** Write simple, beginner-friendly Python with clear variable names and concise comments explaining *why* a block of code exists.

## 2. Mandatory Teaching & Documentation Protocol
- **Incremental Building Only:** Never build more than ONE module or step at a time. Stop after completing the requested step and wait for my approval before moving on.
- **Maintain `ARCHITECTURE.md`:** After every single feature or file change, automatically update `ARCHITECTURE.md` in the root folder. For each module, write in plain, simple English:
  1. What files were created or modified.
  2. Step-by-step data flow (what happens when the user clicks a button).
  3. Why this design/approach was chosen over alternatives (for SIH judge Q&A).
  4. Key edge cases handled.
- **Post-Step Summary:** At the end of every response, give me a 3-bullet summary of the exact logic you just wrote and suggest a descriptive `git commit` message I can run.
