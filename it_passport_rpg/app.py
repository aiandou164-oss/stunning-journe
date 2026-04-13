import streamlit as st
from components import inject_custom_css
import screens

def initialize_session_state():
    defaults = {
        "hp": 100,
        "exp": 0,
        "level": 1,
        "score": 0,
        "combo": 0,
        "mode": None, 
        "screen": "title",
        "current_dungeon": None,
        "question_index": 0,
        "current_questions": [],
        "answered": False,
        "cleared_dungeons": [],
        "wrong_questions": [],
        "mastered_questions": [],
        "start_time": None,
        "exam_results": [],
        "battle_state": {} # For storing current question and answer states
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    st.set_page_config(page_title="測量士補冒険記", page_icon="📐", layout="centered")
    initialize_session_state()
    inject_custom_css()
    
    screen = st.session_state.screen
    if screen == "title":
        screens.show_title_screen()
    elif screen == "dungeon_select":
        screens.show_dungeon_select()
    elif screen == "battle":
        screens.show_battle_screen()
    elif screen == "game_over":
        screens.show_game_over()
    elif screen == "dungeon_clear":
        screens.show_dungeon_clear()
    elif screen == "weakness_select":
        screens.show_weakness_select()
    elif screen == "category_select":
        screens.show_category_select()
    elif screen == "finale":
        screens.show_finale()
    elif screen == "exam_select":
        screens.show_exam_settings()
    elif screen == "exam":
        screens.show_exam_screen()
    elif screen == "exam_result":
        screens.show_exam_result()
    else:
        st.error("Unknown screen state.")
        if st.button("タイトルに戻る"):
            st.session_state.screen = "title"
            st.rerun()

if __name__ == "__main__":
    main()
