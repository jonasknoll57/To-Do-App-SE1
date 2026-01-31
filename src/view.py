import streamlit as st
from datetime import date
from typing import List
from model import Task
from patterns import TaskMediator



COLORS = {
    "primary": "#2563EB",
    "primary_light": "#3B82F6",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger":  "#DC2626",
    "text":    "#0F172A",
    "text_secondary": "#475569",
    "muted":   "#94A3B8",
    "bg":      "#F8FAFC",
    "card":    "#FFFFFF",
    "border":  "#E2E8F0",
}

CSS = f"""
<style>
/* ===== Base ===== */
.stApp {{
  background: {COLORS['bg']};
}}

/* ===== Typography ===== */
.main-header {{
  text-align: center;
  color: {COLORS['text']};
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0.25rem 0 0 0;
}}

.sub-header {{
  text-align: center;
  color: {COLORS['muted']};
  font-size: 0.88rem;
  margin: 0.2rem 0 0.5rem 0;
}}

.section-header {{
  color: {COLORS['text']};
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0.5rem 0 0.5rem 0;
}}

/* ===== Cards / Containers ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {{
  border-radius: 16px !important;
  border-color: {COLORS['border']} !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
}}

/* ===== Inputs ===== */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {{
  border-radius: 10px !important;
}}

.stTextInput input:focus {{
  border-color: {COLORS['primary']} !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}}

/* ===== Buttons ===== */
.stButton > button {{
  border-radius: 10px;
  font-weight: 600;
  padding: 0.45rem 0.75rem;
  transition: all 0.15s ease;
}}

.stButton > button:hover {{
  transform: translateY(-1px);
}}

/* ===== Badge ===== */
.category-badge {{
  background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(37,99,235,0.14));
  color: {COLORS['primary']};
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  display: inline-block;
}}

/* ===== Dates ===== */
.date-overdue {{
  color: {COLORS['danger']};
  font-weight: 650;
  font-size: 0.82rem;
  background: rgba(220,38,38,0.06);
  padding: 1px 8px;
  border-radius: 6px;
}}
.date-today {{
  color: {COLORS['warning']};
  font-weight: 650;
  font-size: 0.82rem;
  background: rgba(217,119,6,0.06);
  padding: 1px 8px;
  border-radius: 6px;
}}
.date-normal {{
  color: {COLORS['text_secondary']};
  font-size: 0.82rem;
}}

/* ===== Done task ===== */
.task-done {{
  text-decoration: line-through;
  color: {COLORS['muted']};
}}

/* ===== Stats Row (compact, inline) ===== */
.stats-row {{
  display: flex;
  justify-content: center;
  gap: 1.2rem;
  flex-wrap: wrap;
  margin: 0.3rem 0;
}}

.stats-item {{
  font-size: 0.82rem;
  color: {COLORS['text_secondary']};
  display: flex;
  align-items: center;
  gap: 4px;
}}

.stats-item b {{
  font-size: 1rem;
  color: {COLORS['text']};
}}

/* ===== Progress ===== */
.progress-bar {{
  background: {COLORS['border']};
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
}}

.progress-fill {{
  background: linear-gradient(90deg, {COLORS['primary']}, #60A5FA);
  height: 100%;
  border-radius: 999px;
  transition: width 0.4s ease;
}}

/* ===== Smart Sort Info ===== */
.smart-info {{
  color: {COLORS['primary']};
  font-size: 0.78rem;
  text-align: center;
  background: rgba(37,99,235,0.05);
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid rgba(37,99,235,0.1);
  margin: 0.25rem 0 0.5rem 0;
}}

/* ===== Empty State ===== */
.empty-list {{
  text-align: center;
  color: {COLORS['muted']};
  padding: 2rem 0;
  font-size: 0.95rem;
}}

/* ===== Task separator ===== */
.task-sep {{
  border: none;
  border-top: 1px solid #F1F5F9;
  margin: 0.3rem 0;
}}

/* ===== Responsive: Tablet ===== */
@media (max-width: 768px) {{
  .main-header {{ font-size: 1.5rem; }}
  .sub-header {{ font-size: 0.82rem; }}
  .stats-item {{ font-size: 0.78rem; }}
  .stats-item b {{ font-size: 0.92rem; }}
}}

/* ===== Responsive: Phone ===== */
@media (max-width: 640px) {{
  .main-header {{ font-size: 1.3rem; }}
  .sub-header {{ display: none; }}
  .section-header {{ font-size: 0.92rem; }}
  .category-badge {{ font-size: 0.65rem; padding: 2px 8px; }}
  .stats-item {{ font-size: 0.72rem; }}
  .stats-item b {{ font-size: 0.85rem; }}
  div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 12px !important;
  }}

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
            st.markdown('<h1 class="main-header">✅ TODO-App</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Öffne die Sidebar, um eine Aufgabe zu erstellen.</p>', unsafe_allow_html=True)
        with c3:
            with st.popover("❓"):
                st.markdown('''
                <div class="help-content">
                <h4>🚀 So funktioniert's</h4>
                <b>Task erstellen:</b> Sidebar links öffnen: Titel eingeben, optional Kategorie & Datum wählen, "Erstellen" klicken.<br><br>
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
            self._header("➕ Neue Aufgabe")

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
                c1, c2, c3 = st.columns([2, 1, 1], gap="small")

                with c1:
                    new_cat = st.text_input(
                        "Neu",
                        key="add_cat_input",
                        placeholder="z.B. Sport",
                        label_visibility="collapsed",
                    )

                with c2:
                    if st.button("➕ Hinzu", key="add_cat_btn", use_container_width=True):
                        if new_cat and new_cat not in st.session_state.categories:
                            st.session_state.categories.append(new_cat)
                            st.rerun()

                with c3:
                    if st.session_state.categories:
                        del_cat = st.selectbox(
                            "Del",
                            st.session_state.categories,
                            key="del_cat_select",
                            label_visibility="collapsed",
                        )
                        if st.button("🗑️", key="del_cat_btn", use_container_width=True):
                            st.session_state.categories.remove(del_cat)
                            st.rerun()

    
    def render_task_section(self):
        """Filter + Task-Liste mit integrierter Statistik."""
        with st.container(border=True):
            self._header("📋 Meine Aufgaben")

            # Kompakte Inline-Statistik
            stats = self.mediator.controller.get_statistics()
            if stats["total"] > 0:
                pct = int(stats['progress'] * 100)
                st.markdown(f'''
                <div class="stats-row">
                    <span class="stats-item">📝 <b>{stats["total"]}</b> Gesamt</span>
                    <span class="stats-item">⏳ <b>{stats["open"]}</b> Offen</span>
                    <span class="stats-item">✅ <b>{stats["done"]}</b> Erledigt</span>
                </div>
                <div style="max-width:260px; margin:0.4rem auto 0.6rem auto;">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width:{pct}%;"></div>
                    </div>
                    <p style="text-align:center; font-size:0.75rem; color:{COLORS['muted']}; margin:0.2rem 0 0 0;">{pct}% erledigt</p>
                </div>
                ''', unsafe_allow_html=True)

            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                status = st.segmented_control("Status", ["Alle", "Offen", "Erledigt"], default="Alle", label_visibility="collapsed", key="status_filter")
                if status is None:
                    status = "Alle"
            with c2:
                cats = ["Alle"] + self.mediator.get_categories()
                cat = st.selectbox("Filter", cats, label_visibility="collapsed")
            with c3:
                st.session_state.smart_sort = st.toggle("🎯", value=st.session_state.smart_sort, help="Smart-Sort: Dringende zuerst")

            st.divider()

            if st.session_state.smart_sort:
                st.markdown('<p class="smart-info">🎯 Sortiert: Überfällig → Heute → Datum</p>', unsafe_allow_html=True)

            tasks = self._get_tasks(status, cat)
            if not tasks:
                st.markdown('<div class="empty-list">🎉 Keine Aufgaben – erstelle eine neue!</div>', unsafe_allow_html=True)
            else:
                for i, task in enumerate(tasks):
                    if i > 0:
                        st.markdown('<hr class="task-sep">', unsafe_allow_html=True)
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

        # Reduzierte, ruhigere Spaltenstruktur
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
            self._header("📊 Fortschritt")


            stats = self.mediator.controller.get_statistics()
            if stats["total"] == 0:
                return
            
            pct = int(stats['progress'] * 100)
            
            # 3 Metrics + Platzhalter (gleiche Breite)
            c1, c2, c3 = st.columns(3)
            c1.metric("📝 Gesamt", stats["total"])
            c2.metric("⏳ Offen", stats["open"])
            c3.metric("✅ Erledigt", stats["done"])

            # Progress mit zentriertem Prozent (gleiche Farbe wie Bar)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f'''
                <div style="text-align: center;">
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

        with st.sidebar:
            self.render_add_task_form()

        self.render_header()
        self.render_task_section()
