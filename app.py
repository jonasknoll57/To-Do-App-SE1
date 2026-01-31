import sys
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_BASE_DIR, "src"))

import streamlit as st
from controller import TaskController
from repository import JSONTaskRepository
from patterns import TaskMediator
from view import TodoView


# Page-Config
st.set_page_config(
    page_title="TODO-App",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def init_app():
    """
    Initialisiert Anwendung
    Session State
    """
    if "mediator" not in st.session_state:
        data_path = os.path.join(_BASE_DIR, "data", "tasks.json")
        repository = JSONTaskRepository(data_path)
        
        controller = TaskController(repository)
        controller.load()
        
        mediator = TaskMediator(controller)
        
        st.session_state.mediator = mediator
    
    return st.session_state.mediator


def main():
    # MVC-Komponenten initialisieren
    mediator = init_app()
    
    view = TodoView(mediator)
    view.render()


if __name__ == "__main__":
    main()
