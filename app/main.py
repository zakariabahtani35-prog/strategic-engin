import streamlit as st
import pandas as pd
import plotly.express as px
import io

import time

from config import Config
from db import init_db, get_db
import crud
from ai_service import ai_engine
import ui_components as ui

import sqlalchemy.exc

# ==========================================
# SYSTEM INITIALIZATION & PROTOCOL
# ==========================================
st.set_page_config(page_title="Strategic Engine", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

try:
    with open("app/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Framework UI Load Failure: {e}")

# Phase 6: DEFENSIVE STARTUP
db_success, db_msg = init_db()
if not db_success:
    st.error("### 🚨 Critical Subsystem Failure")
    st.error(db_msg)
    st.info("The Auto-Repair Engine could not resolve the integrity conflict. Please verify database permissions.")
    st.stop()

if "current_view" not in st.session_state:
    st.session_state.current_view = "Process"

db = get_db()


# ==========================================
# ELITE SIDEBAR / COMMAND STRIP
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <div class='logo-icon'>★</div>
        <div class='logo-text'>Strategic Engine</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='nav-group-label'>Navigation</div>", unsafe_allow_html=True)
    if st.button("❖ Executive Dashboard", use_container_width=True): st.session_state.current_view = "Dashboard"
    if st.button("◎ Process Intelligence", use_container_width=True): st.session_state.current_view = "Process"
    if st.button("✦ Tactical Board", use_container_width=True): st.session_state.current_view = "Tasks"
    

# ==========================================
# PHASE 7: GLOBAL ERROR HANDLER & ROUTER
# ==========================================
try:
    if st.session_state.current_view == "Dashboard":
        ui.render_hero("Executive Dashboard", "Command center for high-level decision intelligence and strategic oversight.")
        
        tasks = crud.get_all_tasks(db)
        meetings = crud.get_recent_meetings(db, limit=20)
        risks = crud.get_all_risks(db)
        decisions = crud.get_all_decisions(db)
        
        if not tasks and not meetings:
            ui.render_empty_state("✨", "Awaiting Intelligence", "Inject your first protocol to populate the command center.")
        else:
            # Strategic Header from last session
            if meetings:
                m = meetings[0]
                ui.render_strategic_header(m.strategic_score, m.overall_sentiment)

            st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1: ui.render_kpi("Intelligence Sessions", str(len(meetings)), "◎ ACTIVE", primary=True)
            with col2: 
                critical_decisions = len([d for d in decisions if d.impact_level.lower() in ['high', 'critical']])
                ui.render_kpi("High-Impact Decisions", str(critical_decisions), "↗ STRATEGIC")
            with col3: 
                high_risk_tasks = len([t for t in tasks if t.failure_probability > 60])
                ui.render_kpi("Risk Vectors", str(high_risk_tasks), "⚠ AT RISK")
            with col4: ui.render_kpi("Detected Threats", str(len(risks)), "↗ MONITORING")
            st.markdown("</div>", unsafe_allow_html=True)
            
            main_col, feed_col = st.columns([2.5, 1])
            with main_col:
                st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title-group'><div class='card-label'>Strategic Decision Matrix</div></div>", unsafe_allow_html=True)
                if decisions:
                    for d in decisions[:5]:
                        ui.render_decision_card(d.decision_text, d.owner, d.confidence_score, d.impact_level, d.ambiguity_reason)
                else:
                    st.write("No decisions recorded yet.")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title-group'><div class='card-label'>Predictive Workload Risk</div></div>", unsafe_allow_html=True)
                if tasks:
                    df = pd.DataFrame([{"Assignee": t.assigned_to, "Failure Risk": t.failure_probability} for t in tasks])
                    fig = px.box(df, x='Assignee', y='Failure Risk', points="all", color_discrete_sequence=['#3b82f6'])
                    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="'Inter', sans-serif"))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with feed_col:
                st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title-group'><div class='card-label'>Memory Feed</div></div>", unsafe_allow_html=True)
                if not meetings: st.write("No active logs.")
                for m in meetings[:5]:
                    dt = m.created_at.strftime("%b %d, %Y")
                    st.markdown(f"""
                    <div style='padding: 1rem 0; border-bottom: 1px solid var(--border-subtle);'>
                        <div style='font-family: "Plus Jakarta Sans"; font-weight: 700; font-size: 0.95rem; color: var(--navy-900);'>{m.title}</div>
                        <div style='color: var(--text-tertiary); font-size: 0.75rem; margin-top: 0.4rem;'><span style='padding:0.2rem 0.4rem; background:rgba(0,0,0,0.05); border-radius:4px;'>{dt}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # VIEW: PROCESS INTELLIGENCE
    # ==========================================
    elif st.session_state.current_view == "Process":
        ui.render_processor_hero()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='saas-card' style='padding: 3rem;'>", unsafe_allow_html=True)
        
        col_input, col_insights = st.columns([2.2, 1], gap="large")
        extracted_file_text = ""
        file_status = "--"
        file_bytes = 0
        
        with col_input:
            st.markdown("<h3 style='margin-bottom: 1.5rem;'>Strategic Data Ingestion</h3>", unsafe_allow_html=True)
            m_title = st.text_input("Operational Designation *", placeholder="e.g. Q3 Roadmap Planning")
            uploaded_file = st.file_uploader("Upload Telemetry File", type=["txt", "csv"], label_visibility="collapsed")
            if uploaded_file:
                # ... (Existing processing logic same)
                file_bytes = uploaded_file.size
                extracted_file_text = uploaded_file.read().decode('utf-8')
                file_status = f"Secured ({uploaded_file.name})"
            
            raw_text = st.text_area("Manual Input Overflow", height=200)
            target_payload = extracted_file_text if extracted_file_text.strip() else raw_text

        with col_insights:
            ui.render_kpi("Ingest Status", file_status if file_status != "--" else "Awaiting", trend="")
            st.info("System Engine will analyze context, detect mandates, and forecast execution risks.")
            
        if st.button("Execute Intelligence Analysis", type="primary"):
            if m_title and target_payload:
                with st.spinner("Synthesizing Strategic Intelligence..."):
                    response = ai_engine.analyze_meeting(target_payload)
                    if response["success"]:
                        result = response["data"]
                        meeting_record = crud.create_full_meeting_record(db, m_title, target_payload, result)
                        if meeting_record:
                            st.balloons()
                            ui.render_strategic_header(result.get('strategic_score', 50), result.get('overall_sentiment', 'Neutral'))
                            ui.render_executive_brief(result.get('executive_summary'))
                            
                            t1, t2, t3, t4 = st.tabs(["❖ Decisions", "◎ Action", "⚠ Risks", "✦ Synthesis"])
                            with t1:
                                for d in result.get('decisions', []):
                                    ui.render_decision_card(d.get('decision'), d.get('owner'), d.get('confidence_score'), d.get('impact_level'), d.get('ambiguity_reason'))
                            with t2:
                                for t in result.get('tasks', []):
                                    ui.render_task_row(t.get('task'), t.get('assigned_to'), t.get('deadline'), t.get('priority'), "Pending", t.get('failure_probability', 0))
                            with t3:
                                ui.render_insight_list(meeting_record.risks, "risk")
                            with t4:
                                st.write(result.get('detailed_summary'))
                    else:
                        st.error(f"Analysis Failed: {response['error_message']}")

    # ==========================================
    # VIEW: TACTICAL BOARD
    # ==========================================
    elif st.session_state.current_view == "Tasks":
        ui.render_hero("Tactical Board", "Operational queue with predictive risk weighting.")
        tasks = crud.get_all_tasks(db)
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        if not tasks:
            ui.render_empty_state("◎", "Matrix Clear", "Operational queue is empty.")
        else:
            for t in tasks:
                col1, col2 = st.columns([5, 1])
                with col1:
                    ui.render_task_row(t.task_description, t.assigned_to, t.deadline, t.priority, t.status, t.failure_probability)
                with col2:
                    if st.button("Purge", key=f"del_{t.id}"):
                        crud.remove_task(db, t.id)
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except sqlalchemy.exc.OperationalError as e:
    st.error("### 🔧 Database Integrity Mismatch Detected")
    st.warning("The application attempted to read a schema column that doesn't exist.")
    st.info("💡 **Auto-Repair System Engaged:** The background `init_db()` auto-repair engine failed to lock the schema. Please restart the app to allow the Self-Healing engine to dynamically inject missing columns.")
    with st.expander("Show Operational Trace"):
        st.code(str(e))
