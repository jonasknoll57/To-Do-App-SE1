import streamlit as st
from controller import TaskController
from repository import JSONTaskRepository
from patterns import TaskMediator
from view import TodoView


# Config
st.set_page_config(
    page_title="TODO-App",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisierung
def init_app():
    if "mediator" not in st.session_state:
        repository = JSONTaskRepository("tasks.json")
        
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
