import streamlit as st
from datetime import date
from typing import List
from model import Task
from patterns import TaskMediator



COLORS = {
    # Primär – Rot (Streamlit Red als Anker)
    "primary":        "#FF4B4B",   # Streamlit Red – Buttons, aktive Elemente
    "primary_hover":  "#E63E3E",   # Red 600      – Hover
    "primary_light":  "#FEF2F2",   # Red 50       – Section-Header, Badge-Hintergrund
    "primary_soft":   "#FCA5A5",   # Red 300      – Gradient-Endpunkt

    # Semantische Farben (jeweils mit heller Variante)
    "success":        "#059669",   # Emerald 600  – Erledigt
    "success_light":  "#ECFDF5",   # Emerald 50
    "warning":        "#D97706",   # Amber 600    – Heute fällig
    "warning_light":  "#FFFBEB",   # Amber 50
    "danger":         "#991B1B",   # Red 800      – Überfällig, Löschen (dunkler als Primary)
    "danger_light":   "#FEE2E2",   # Red 100

    # Neutrale – Gray (neutral, lässt Rot wirken)
    "text":           "#111827",   # Gray 900   – Primärtext
    "text_secondary": "#4B5563",   # Gray 600   – Sekundärtext
    "muted":          "#9CA3AF",   # Gray 400   – Platzhalter, deaktiviert
    "bg":             "#FAFAFA",   # Neutral 50 – App-Hintergrund
    "card":           "#FFFFFF",   # Weiß       – Karten, Container
    "border":         "#E5E7EB",   # Gray 200   – Rahmen, Trennlinien
}

CSS = f"""
<style>
.stApp {{
  background: {COLORS['bg']};
  color: {COLORS['text']};
}}

html, body, [class*="css"] {{
  font-size: 16px;
}}

/* --- Header --- */
.main-header {{
  text-align: center;
  color: {COLORS['text']};
  font-size: 1.9rem;
  font-weight: 750;
  margin: 0.25rem 0 0 0;
}}
.sub-header {{
  text-align: center;
  color: {COLORS['text_secondary']};
  font-size: 0.95rem;
  margin: 0.35rem 0 1.0rem 0;
}}
.section-header {{
  text-align: center;
  color: {COLORS['primary']};
  font-size: 1.05rem;
  font-weight: 650;
  margin: 0 0.5rem 0.75rem 0.5rem;
  padding: 0.6rem 1rem;
  background: {COLORS['primary_light']};
  border-radius: 10px;
}}
.filter-label {{
  color: {COLORS['text_secondary']};
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.3rem;
}}

/* --- Metric-Karten --- */
div[data-testid="stMetric"] {{
  background: {COLORS['card']};
  border: 1px solid {COLORS['border']};
  border-radius: 12px;
  padding: 0.75rem;
  box-shadow: 0 1px 3px rgba(15,23,42,0.04), 0 1px 2px rgba(15,23,42,0.02);
}}
div[data-testid="stMetric"] label {{
  font-size: 0.8rem !important;
  color: {COLORS['text_secondary']} !important;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
  font-size: 1.6rem !important;
  color: {COLORS['text']} !important;
}}

/* --- Inputs / Buttons --- */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {{
  border-radius: 10px !important;
  border-color: {COLORS['border']} !important;
}}
.stButton > button {{
  border-radius: 10px;
  font-weight: 600;
  padding: 0.45rem 0.75rem;
}}

/* --- Kategorie-Badge (Pill) --- */
.category-badge {{
  background: {COLORS['primary_light']};
  color: {COLORS['primary']};
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  display: inline-block;
}}

/* --- Datum-Labels (Pill-Stil mit Hintergrund) --- */
.date-overdue {{
  background: {COLORS['danger_light']};
  color: {COLORS['danger']};
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 650;
  font-size: 0.78rem;
}}
.date-today {{
  background: {COLORS['warning_light']};
  color: {COLORS['warning']};
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 650;
  font-size: 0.78rem;
}}
.date-normal {{
  color: {COLORS['text_secondary']};
  font-size: 0.82rem;
}}

/* --- Erledigter Task --- */
.task-done {{
  text-decoration: line-through;
  color: {COLORS['muted']};
}}

/* --- Task-Zeile --- */
.task-row {{
  padding: 0.35rem 0;
}}

/* --- Fortschrittsbalken (Gradient) --- */
.progress-bar {{
  background: {COLORS['border']};
  border-radius: 999px;
  height: 10px;
  overflow: hidden;
}}
.progress-fill {{
  background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['primary_soft']});
  height: 100%;
  border-radius: 999px;
  transition: width 0.4s ease;
}}

/* --- Smart-Sort Info --- */
.smart-info {{
  color: {COLORS['text_secondary']};
  font-size: 0.8rem;
  text-align: center;
  margin: 0.25rem 0 0.75rem 0;
}}

/* --- Leere Liste --- */
.empty-list {{
  text-align: center;
  color: {COLORS['muted']};
  padding: 2rem 0;
  font-size: 0.95rem;
}}

/* --- Lösch-Warnung --- */
.delete-warning {{
  color: {COLORS['danger']};
  font-weight: 600;
  font-size: 0.9rem;
}}

/* --- Mobile --- */
@media (max-width: 640px) {{
  .main-header {{ font-size: 1.6rem; }}
  .sub-header {{ font-size: 0.9rem; }}
  .category-badge {{ font-size: 0.65rem; }}
}}
</style>
"""



class TodoView:
    
    def __init__(self, mediator: TaskMediator):
        self.mediator = mediator
        self._init_session_state()
    
    def _init_session_state(self):
        defaults = {"edit_id": None, "categories": ["Arbeit", "Privat", "Einkauf", "Sonstiges"], "smart_sort": True}
        for key, val in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = val
    
    def _header(self, text: str):
        """zentrierte Überschrift"""
        st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)
    
    def render_header(self):
        """App-Header mit Hilfe-Button."""
        c1, c2, c3 = st.columns([1, 6, 1])
        with c2:
            st.markdown('<h1 class="main-header">TODO-App</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Organisiere deine Aufgaben einfach und effizient</p>', unsafe_allow_html=True)
        with c3:
            with st.popover("❓"):
                st.markdown('''
                <div class="help-content">
                <h4>🚀 So funktioniert's</h4>
                <b>Task erstellen:</b> Titel eingeben, optional Kategorie & Datum wählen, "Erstellen" klicken.<br><br>
                <b>Task erledigen:</b> Checkbox anklicken.<br><br>
                <b>Task bearbeiten:</b> ✏️ klicken, ändern, speichern.<br><br>
                <b>Task löschen:</b> 🗑️ klicken und bestätigen.<br><br>
                <h4>🎯 Smart-Sortierung</h4>
                Aktiviere den Toggle um dringende Tasks automatisch oben zu sehen:<br>
                1. Überfällige Tasks<br>
                2. Heute fällige<br>
                3. Zukünftige (nach Datum)<br>
                4. Erledigte Tasks
                </div>
                ''', unsafe_allow_html=True)
    
    def render_add_task_form(self):
        """Formular zum Hinzufügen neuer Tasks (neu sortiert)."""
        with st.container(border=True):
            self._header("Neue Aufgabe hinzufügen")

            _, form_col, _ = st.columns([0.3, 9.4, 0.3])
            with form_col:
                # 1) 2er Container: Aufgabenname + Datum
                r1c1, r1c2 = st.columns([3, 2], gap="medium")
                with r1c1:
                    new_title = st.text_input(
                        "Titel",
                        placeholder="Was möchtest du erledigen?",
                        label_visibility="collapsed",
                        key="new_task_input",
                    )
                with r1c2:
                    new_due = st.date_input(
                        "Datum",
                        value=None,
                        min_value=date.today(),
                        label_visibility="collapsed",
                        key="new_due",
                    )

                # 2) 1er: Kategorie (volle Breite)
                cat_options = ["Kategorie..."] + st.session_state.categories
                cat_idx = st.selectbox(
                    "Kategorie",
                    options=range(len(cat_options)),
                    format_func=lambda i: cat_options[i],
                    label_visibility="collapsed",
                    key="new_cat",
                    index=0,
                )
                new_category = "" if cat_idx == 0 else cat_options[cat_idx]

                # 3) 1er: Erstellen (volle Breite)
                if st.button(
                    "Erstellen",
                    type="primary",
                    use_container_width=True,
                    help="Task erstellen",
                    key="create_task_btn",
                ):
                    if new_title:
                        self.mediator.add_task(new_title, category=new_category, due_date=new_due)
                        st.rerun()
                    else:
                        st.toast("⚠️ Bitte Titel eingeben")

                # 4) 1er: Kategorien verwalten (volle Breite)
                with st.expander("📁 Kategorien verwalten", expanded=False):
                    c1, c2 = st.columns([2, 1], gap="small")

                    with c1:
                        new_cat = st.text_input(
                            "Neu",
                            key="add_cat_input",
                            placeholder="z.B. Sport",
                            label_visibility="collapsed",
                        )
                        if st.button("➕ Hinzufügen", key="add_cat_btn", use_container_width=True):
                            if new_cat and new_cat not in st.session_state.categories:
                                st.session_state.categories.append(new_cat)
                                st.rerun()

                    with c2:
                        if st.session_state.categories:
                            del_cat = st.selectbox(
                                "Del",
                                st.session_state.categories,
                                key="del_cat_select",
                                label_visibility="collapsed",
                            )
                            if st.button("🗑️ Löschen", key="del_cat_btn", use_container_width=True):
                                st.session_state.categories.remove(del_cat)
                                st.rerun()

    
    def render_task_section(self):
        """Filter + Task-Liste kombiniert."""
        with st.container(border=True):
            self._header("Meine Aufgaben")

            st.markdown('<p class="filter-label">Filter</p>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3, 2, 1], vertical_alignment="center")
            with c1:
                status = st.segmented_control(
                    "Status",
                    options=["Alle", "Offen", "Erledigt"],
                    default="Alle",
                    label_visibility="collapsed",
                    key="status_filter",
                )
                if status is None:
                    status = "Alle"
            with c2:
                cats = ["Alle Kategorien"] + self.mediator.get_categories()
                cat_sel = st.selectbox("Kategorie", cats, label_visibility="collapsed")
                cat = "Alle" if cat_sel == "Alle Kategorien" else cat_sel
            with c3:
                st.session_state.smart_sort = st.toggle("🎯", value=st.session_state.smart_sort, help="Smart-Sort: Dringende zuerst")

            if st.session_state.smart_sort:
                st.markdown('<p class="smart-info">🎯 Überfällig → Heute → Datum</p>', unsafe_allow_html=True)

            tasks = self._get_tasks(status, cat)
            if not tasks:
                st.markdown('<div class="empty-list">🎉 Keine Aufgaben – erstelle eine neue!</div>', unsafe_allow_html=True)
            else:
                _, task_col, _ = st.columns([0.3, 9.4, 0.3])
                with task_col:
                    for task in tasks:
                        if st.session_state.edit_id == task.id:
                            self._render_edit_form(task)
                        else:
                            self._render_task_item(task)
    
    def _get_tasks(self, status: str, category: str) -> List[Task]:
        """Gibt gefilterte Task-Liste zurück."""
        if status == "Offen": tasks = self.mediator.get_open_tasks()
        elif status == "Erledigt": tasks = self.mediator.get_done_tasks()
        else: tasks = self.mediator.get_all_tasks()
        
        if category != "Alle":
            tasks = [t for t in tasks if t.category == category]
        
        if st.session_state.smart_sort:
            def key(t):
                if t.done: return (4, date.max)
                if t.is_overdue(): return (0, t.due_date)
                if t.is_due_today(): return (1, t.due_date)
                if t.due_date: return (2, t.due_date)
                return (3, date.max)
            tasks = sorted(tasks, key=key)
        return tasks
    
    def _render_task_item(self, task: Task):
        """
        Rendert ein Task-Item:
        Checkbox | Titel + Meta (Kategorie + Datum) | Edit | Delete
        """

        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([0.5, 4.5, 0.7, 0.7], gap="small")

            # Checkbox
            with c1:
                checked = st.checkbox(
                    "done",
                    value=task.done,
                    key=f"cb_{task.id}",
                    label_visibility="collapsed"
                )
                if checked != task.done:
                    self.mediator.toggle_task(task.id)
                    st.rerun()

            # Titel + Meta
            with c2:
                title_class = "task-done" if task.done else ""
                st.markdown(
                    f'<div class="{title_class}">{task.title}</div>',
                    unsafe_allow_html=True
                )

                # Meta-Zeile (Kategorie · Datum)
                meta_parts = []

                if task.category:
                    meta_parts.append(
                        f'<span class="category-badge">{task.category}</span>'
                    )

                if task.due_date and not task.done:
                    if task.is_overdue():
                        meta_parts.append(
                            f'<span class="date-overdue">⚠️ {task.due_date.strftime("%d.%m.")}</span>'
                        )
                    elif task.is_due_today():
                        meta_parts.append(
                            '<span class="date-today">📅 Heute</span>'
                        )
                    else:
                        meta_parts.append(
                            f'<span class="date-normal">📅 {task.due_date.strftime("%d.%m.")}</span>'
                        )

                if meta_parts:
                    st.markdown(
                        '<div style="margin-top:2px; display:flex; gap:8px; align-items:center;">'
                        + "".join(meta_parts) +
                        '</div>',
                        unsafe_allow_html=True
                    )

            # Edit
            with c3:
                if st.button("✏️", key=f"edit_{task.id}", use_container_width=True):
                    st.session_state.edit_id = task.id
                    st.rerun()

            # Delete
            with c4:
                with st.popover("🗑️", use_container_width=True):
                    st.markdown(
                        '<p class="delete-warning">⚠️ Wirklich endgültig löschen?</p>',
                        unsafe_allow_html=True
                    )
                    st.caption(f'"{task.title}"')
                    if st.button(
                        "🗑️ Ja, löschen",
                        key=f"confirm_del_{task.id}",
                        use_container_width=True
                    ):
                        self.mediator.delete_task(task.id)
                        st.rerun()

    
    def _render_edit_form(self, task: Task):
        """Bearbeitungs-Formular kompakt."""
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                title = st.text_input("Titel", value=task.title, key=f"edit_title_{task.id}", label_visibility="collapsed")
            with c2:
                cat_opts = ["Keine"] + st.session_state.categories
                cat_idx = cat_opts.index(task.category) if task.category in cat_opts else 0
                cat = st.selectbox("Kat", cat_opts, index=cat_idx, key=f"edit_cat_{task.id}", label_visibility="collapsed")
                cat = "" if cat == "Keine" else cat
            with c3:
                due = st.date_input("Datum", value=task.due_date, key=f"edit_due_{task.id}", label_visibility="collapsed")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Speichern", key=f"save_{task.id}", type="primary", use_container_width=True):
                    self.mediator.update_task(task.id, title=title, category=cat, due_date=due)
                    st.session_state.edit_id = None
                    st.rerun()
            with c2:
                if st.button("❌ Abbruch", key=f"cancel_{task.id}", use_container_width=True):
                    st.session_state.edit_id = None
                    st.rerun()
    
    def render_statistics(self):
        """Kompakte Statistik-Sektion mit Fortschritt."""
        with st.container(border=True):
            self._header("Fortschritt")

            stats = self.mediator.controller.get_statistics()
            if stats["total"] == 0:
                return

            pct = int(stats['progress'] * 100)

            _, stats_col, _ = st.columns([0.3, 9.4, 0.3])
            with stats_col:
                c1, c2, c3 = st.columns(3)
                c1.metric("📝 Gesamt", stats["total"])
                c2.metric("⏳ Offen", stats["open"])
                c3.metric("✅ Erledigt", stats["done"])

                # Progress mit zentriertem Prozent
                col1, col2, col3 = st.columns([0.5, 3, 0.5])
                with col2:
                    st.markdown(f'''
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 1.5em; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 8px;">
                            {pct}%
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {pct}%;"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    def render(self):
        st.markdown(CSS, unsafe_allow_html=True)

        self.render_header()

        left_col, right_col = st.columns([1.2, 2], gap="large")

        with left_col:
            self.render_add_task_form()
            st.space()
            self.render_statistics()
            
        with right_col:
            self.render_task_section()
