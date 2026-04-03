import streamlit as st

def render_hero(title: str, subtitle: str):
    """Renders a standard premium Hero Header."""
    html = f"""
    <div class="hero-header">
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_processor_hero():
    """Renders the dramatic, glowing AI Command Header."""
    html = """
    <div class="processor-hero">
        <h1>Intelligence Processor</h1>
        <p>Command center for telemetry analysis, context generation, and operational delegation.</p>
        <div class="status-chip-row">
            <div class="status-chip emerald"><span class="dot"></span> AI Engine Online</div>
            <div class="status-chip cyan"><span class="dot"></span> Processing Matrix Active</div>
            <div class="status-chip purple"><span class="dot"></span> Data Pipeline Ready</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_strategic_header(score: int, sentiment: str):
    """Renders the top-level Strategic Impact header with a visual score gauge."""
    color = "var(--accent-emerald)" if score > 70 else "var(--accent-blue)" if score > 40 else "var(--accent-rose)"
    icon = "↗" if sentiment.lower() in ['positive', 'growth'] else "↘" if sentiment.lower() in ['negative', 'contention'] else "→"
    
    html = f"""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 2.5rem; padding: 2rem; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-ambient);'>
        <div>
            <div style='text-transform:uppercase; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.1em; color: var(--text-tertiary); margin-bottom: 0.5rem;'>Strategic Impact Assessment</div>
            <div style='display:flex; align-items:center; gap: 0.75rem;'>
                <span style='font-size: 2.5rem; font-weight: 800; font-family: "Plus Jakarta Sans";'>{score}%</span>
                <span style='padding: 0.4rem 0.8rem; background:rgba(0,0,0,0.05); border-radius: 8px; font-weight: 700; color: {color}; font-size: 0.9rem;'>{icon} {sentiment.upper()}</span>
            </div>
        </div>
        <div style='width: 200px; height: 12px; background: rgba(0,0,0,0.05); border-radius: 30px; overflow: hidden; position: relative;'>
            <div style='width: {score}%; height: 100%; background: {color}; border-radius: 30px; box-shadow: 0 0 15px {color};'></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_executive_brief(content: str):
    """Renders the highly styled Executive Output card."""
    html = f"""
    <div class="executive-brief-card">
        <h3>Executive Synthesis</h3>
        <p>{content}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_kpi(title: str, value: str, trend: str = "", primary: bool = False):
    """Renders high-fidelity KPI metric cards."""
    cl = "metric-card alpha" if primary else "metric-card"
    trend_html = f"<div class='metric-trend'>{trend}</div>" if trend else ""
    
    html = f"""
    <div class="{cl}">
        <div class="metric-title">
            {title}
        </div>
        <div class="metric-value">{value}</div>
        {trend_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_pill(text: str, category: str = "prio"):
    """Renders elite-level pill badges with indicator dots."""
    if not text: return ""
    norm = text.lower().strip()
    
    if category == "prio":
        if "high" in norm: c = "pill-high"
        elif "low" in norm: c = "pill-low"
        else: c = "pill-mid"
    else:
        if "done" in norm: c = "pill-done"
        elif "progress" in norm: c = "pill-progress"
        else: c = "pill-pending"
        
    return f"""
    <span class='premium-pill {c}'>
        <span class='pill-indicator'></span>
        {text}
    </span>
    """

def render_decision_card(text: str, owner: str, confidence: int, impact: str, ambiguity: str = ""):
    """Renders a Decision Matrix card with clarity and impact states."""
    conf_color = "var(--accent-emerald)" if confidence > 80 else "var(--accent-cyan)" if confidence > 50 else "var(--accent-rose)"
    impact_cl = f"pill-{impact.lower()}" if impact.lower() in ['high', 'mid', 'low'] else "pill-high" if impact.lower() == 'critical' else "pill-mid"
    
    ambiguity_html = f"<div style='margin-top: 1rem; padding: 0.75rem; background: rgba(225, 29, 72, 0.05); border-left: 3px solid var(--accent-rose); font-size: 0.85rem; color: #be123c;'><strong>Ambiguity Detected:</strong> {ambiguity}</div>" if ambiguity else ""
    
    html = f"""
    <div style='background: white; border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1.5rem; margin-bottom: 1rem; transition: transform 0.2s ease;' onmouseover="this.style.transform='translateX(4px)'" onmouseout="this.style.transform='translateX(0)'">
        <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 1rem;'>
            <div style='font-weight: 700; font-family: "Plus Jakarta Sans"; font-size: 1.1rem; color: var(--navy-900); max-width: 80%;'>{text}</div>
            <span class='premium-pill {impact_cl}' style='font-size: 0.65rem;'>{impact.upper()} IMPACT</span>
        </div>
        <div style='display:flex; gap: 1.5rem; font-size: 0.85rem; color: var(--text-secondary);'>
            <span><strong>Owner:</strong> {owner}</span>
            <span style='color: {conf_color}; font-weight: 700;'>Confidence: {confidence}%</span>
        </div>
        {ambiguity_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_task_row(title: str, assignee: str, deadline: str, priority: str, status: str, risk: int = 0):
    """Renders an analytical task row with failure probability forecasting."""
    prio_html = render_pill(priority, "prio")
    stat_html = render_pill(status, "stat")
    
    risk_color = "var(--accent-emerald)" if risk < 30 else "var(--accent-cyan)" if risk < 60 else "var(--accent-rose)"
    
    html = f"""
    <div class="entity-row">
        <div class="entity-main">
            <div style='display:flex; align-items:center; gap: 1rem;'>
                <div class="entity-title">{title}</div>
                <div style='font-size: 0.7rem; font-weight: 800; color: {risk_color}; background: rgba(0,0,0,0.03); padding: 0.2rem 0.5rem; border-radius: 4px;'>{risk}% FAILURE RISK</div>
            </div>
            <div class="entity-meta">
                <span><strong>Delegated To:</strong> {assignee}</span>
                <span><strong>Target:</strong> {deadline}</span>
            </div>
        </div>
        <div class="entity-actions">
            {prio_html}
            {stat_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_insight_list(items: list, insight_type: str = "step"):
    """Renders elegant insight bullets matching the 'Strategic Engine' aesthetic."""
    if not items:
        st.markdown("<p style='color: #94a3b8; font-style: italic; font-size: 0.95rem; padding: 1rem;'>No intelligence available.</p>", unsafe_allow_html=True)
        return
        
    for item in items:
        # Compatibility with old string format and new objects
        val = getattr(item, 'risk_text', getattr(item, 'step_text', str(item)))
        level = getattr(item, 'risk_level', 'Moderate') if insight_type == "risk" else ""
        strategy = getattr(item, 'prevention_strategy', '') if insight_type == "risk" else ""
        
        icon = "⚠" if insight_type == "risk" else "◎"
        
        detail_html = f"<div style='font-size: 0.8rem; color: var(--text-tertiary); margin-top: 0.4rem;'>{strategy}</div>" if strategy else ""
        badge_html = f"<span style='font-size: 0.6rem; font-weight: 800; color: white; background: var(--accent-rose); padding: 0.1rem 0.4rem; border-radius: 3px; margin-left: 0.5rem;'>{level.upper()}</span>" if level and level != "Moderate" else ""

        html = f"""
        <div class="strategic-item {insight_type}">
            <div class="item-bullet {insight_type}">{icon}</div>
            <div style='width: 100%'>
                <div style='font-weight: 600;'>{val}{badge_html}</div>
                {detail_html}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

def render_empty_state(icon: str, title: str, message: str):
    """Renders a spacious, high-contrast Empty State."""
    html = f"""
    <div style="text-align: center; padding: 5rem 2rem; background: transparent; border-radius: 24px; border: 1px dashed var(--border-focus); margin-top: 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 1.5rem; filter: saturate(0); opacity: 0.6;">{icon}</div>
        <h3 style="color: var(--navy-900); margin-bottom: 0.5rem; font-size: 1.25rem;">{title}</h3>
        <p style="color: var(--text-secondary); max-width: 400px; margin: 0 auto; font-size: 0.95rem;">{message}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
