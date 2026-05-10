import streamlit as st
import json

st.set_page_config(
    page_title="Bengaluru Events 🎉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e); min-height: 100vh; }

  /* Hero */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
  }
  .hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }
  .hero p { color: #94a3b8; font-size: 1.1rem; }

  /* Filter pills */
  .filter-bar {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    justify-content: center; margin: 1.5rem 0;
  }

  /* Event card */
  .event-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.4rem 1.4rem 1rem;
    margin-bottom: 1.2rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
  }
  .event-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    border-radius: 16px 16px 0 0;
  }
  .event-card:hover {
    border-color: rgba(167,139,250,0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(167,139,250,0.15);
  }
  .event-title {
    font-size: 1.05rem; font-weight: 700; color: #e2e8f0;
    margin-bottom: 0.5rem; line-height: 1.3;
  }
  .event-meta { color: #94a3b8; font-size: 0.82rem; margin-bottom: 0.3rem; }
  .event-meta span { margin-right: 1rem; }

  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-right: 4px;
    margin-top: 6px;
  }
  .badge-vibe  { background: rgba(167,139,250,0.18); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }
  .badge-net   { background: rgba(96,165,250,0.18);  color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
  .badge-fee   { background: rgba(52,211,153,0.18);  color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
  .badge-intro { background: rgba(251,191,36,0.18);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }

  .section-header {
    color: #e2e8f0; font-size: 1.3rem; font-weight: 700;
    margin: 2rem 0 1rem; display: flex; align-items: center; gap: 0.5rem;
  }
  .count-badge {
    background: rgba(167,139,250,0.2); color: #a78bfa;
    padding: 2px 12px; border-radius: 999px; font-size: 0.85rem;
  }

  /* Question card */
  .q-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1.5rem 1.5rem 0.5rem;
    margin-bottom: 1.2rem;
  }
  .q-label { color: #e2e8f0; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.8rem; }

  /* Streamlit widget overrides */
  .stMultiSelect [data-baseweb="tag"] { background: rgba(167,139,250,0.25) !important; }
  .stSelectbox div[data-baseweb="select"] > div { background: rgba(255,255,255,0.06) !important; }
  div[data-testid="stButton"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  div[data-testid="stButton"] button:hover { transform: translateY(-1px); }

  .no-results {
    text-align: center; color: #64748b;
    padding: 3rem; font-size: 1.1rem;
  }
  hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)


from pathlib import Path

@st.cache_data
def load_events():
    candidates = [
        Path(__file__).parent / "cleaned_events.json",
        Path.cwd() / "cleaned_events.json",
    ]
    for path in candidates:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for e in data:
                e.setdefault("fee", "")
                e.setdefault("source", "")
                e.setdefault("vibe", "General")
                e.setdefault("introvert_friendly", False)
                e.setdefault("networking_level", "Medium")
                e.setdefault("best_for", [])
                e.setdefault("description", "")
                e.setdefault("image_url", "")
                e.setdefault("organizer", "")
                e.setdefault("link", "#")
            return data
    return None

EVENTS = load_events()

if EVENTS is None:
    st.error(
        "⚠️ **`cleaned_events.json` not found.**\n\n"
        "Make sure the file is in the **same folder** as `event_app.py`, then restart the app.",
        icon="🗂️",
    )
    st.stop()

def score_event(event, interests, social_pref, free_only, networking_pref):
    score = 0
    vibe_lower = event["vibe"].lower()
    best_lower = " ".join(event["best_for"]).lower()

    for interest in interests:
        kw = interest.lower()
        if kw in vibe_lower or kw in best_lower or kw in event["title"].lower():
            score += 3

    if social_pref == "Introvert (small/quiet)" and event["introvert_friendly"]:
        score += 2
    elif social_pref == "Extrovert (big & social)" and not event["introvert_friendly"]:
        score += 2
    elif social_pref == "No preference":
        score += 1

    if free_only and event["fee"] != "Free":
        return -1  # exclude

    net_map = {"Low": 1, "Medium": 2, "High": 3}
    pref_map = {"Not important": 1, "Some networking is fine": 2, "Heavy networking": 3}
    net_score = net_map.get(event["networking_level"], 2)
    pref_score = pref_map.get(networking_pref, 2)
    if abs(net_score - pref_score) == 0:
        score += 2
    elif abs(net_score - pref_score) == 1:
        score += 1

    return score

def render_event_card(event, idx):
    fee_badge = f'<span class="badge badge-fee">Free</span>' if event["fee"] == "Free" else ""
    intro_badge = '<span class="badge badge-intro">👤 Introvert-friendly</span>' if event["introvert_friendly"] else ""
    net_color = {"Low": "badge-fee", "Medium": "badge-net", "High": "badge-vibe"}.get(event["networking_level"], "badge-net")
    net_badge = f'<span class="badge {net_color}">🤝 {event["networking_level"]} networking</span>'
    source_icon = "🟣" if event["source"] == "Luma" else "🟠"

    st.markdown(f"""
    <div class="event-card">
      <div style="display:flex; gap:1rem; align-items:flex-start;">
        <img src="{event['image_url']}" style="width:64px;height:64px;border-radius:12px;object-fit:cover;flex-shrink:0;" onerror="this.style.display='none'">
        <div style="flex:1; min-width:0;">
          <div class="event-title">{event['title']}</div>
          <div class="event-meta">
            <span>📅 {event['date']}</span>
            <span>📍 {event['location']}</span>
            {f'<span>👤 {event["organizer"]}</span>' if event['organizer'] else ''}
          </div>
          <div class="event-meta" style="margin-top:2px;">{source_icon} {event['source']}</div>
          <div style="margin-top:6px;">
            <span class="badge badge-vibe">✨ {event['vibe']}</span>
            {net_badge}{fee_badge}{intro_badge}
          </div>
          <div style="color:#94a3b8; font-size:0.82rem; margin-top:8px;">{event['description']}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        f"🎟️ View & Register →",
        event["link"],
        use_container_width=True,
    )
    st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎯 Bengaluru Events</h1>
  <p>Discover events tailored to <em>your</em> vibe — May 2026</p>
</div>
""", unsafe_allow_html=True)

if "show_all" not in st.session_state:
    st.session_state.show_all = False

with st.sidebar:
    st.markdown("### 🎨 Personalise Your Feed")
    st.markdown("---")

    st.markdown('<div class="q-label">What are you into?</div>', unsafe_allow_html=True)
    interests = st.multiselect(
        "Select your interests",
        ["AI", "Tech", "Startup", "Networking", "Education", "Finance",
         "Crypto / Web3", "Career", "Data Science", "Fitness", "Community"],
        default=["AI", "Tech"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="q-label">What\'s your social style?</div>', unsafe_allow_html=True)
    social_pref = st.radio(
        "Social style",
        ["Introvert (small/quiet)", "No preference", "Extrovert (big & social)"],
        index=1,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="q-label">How important is networking to you?</div>', unsafe_allow_html=True)
    networking_pref = st.select_slider(
        "Networking importance",
        options=["Not important", "Some networking is fine", "Heavy networking"],
        value="Some networking is fine",
        label_visibility="collapsed"
    )

    st.markdown("---")
    free_only = st.toggle("🆓 Show free events only", value=False)

    st.markdown("---")
    find_btn = st.button("✨ Find My Events", use_container_width=True, type="primary")
    show_all_btn = st.button("📋 Show All Events", use_container_width=True)

    if show_all_btn:
        st.session_state.show_all = True
    if find_btn:
        st.session_state.show_all = False

if st.session_state.show_all:
    st.markdown(f"""
    <div class="section-header">
      📋 All Events <span class="count-badge">{len(EVENTS)}</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, event in enumerate(EVENTS):
        with cols[i % 2]:
            render_event_card(event, i)

else:
    # Score and filter
    scored = []
    for e in EVENTS:
        s = score_event(e, interests, social_pref, free_only, networking_pref)
        if s >= 0:
            scored.append((s, e))
    scored.sort(key=lambda x: -x[0])

    top = [(s, e) for s, e in scored if s >= 3]
    rest = [(s, e) for s, e in scored if s < 3]

    if not scored:
        st.markdown('<div class="no-results">😅 No events match your filters. Try removing the free-only filter or broadening your interests.</div>', unsafe_allow_html=True)
    else:
        if top:
            st.markdown(f"""
            <div class="section-header">
              🌟 Recommended for You <span class="count-badge">{len(top)}</span>
            </div>
            """, unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (score, event) in enumerate(top):
                with cols[i % 2]:
                    render_event_card(event, i)

        if rest:
            st.markdown(f"""
            <div class="section-header">
              🗓️ Other Events <span class="count-badge">{len(rest)}</span>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Show other events", expanded=False):
                cols = st.columns(2)
                for i, (score, event) in enumerate(rest):
                    with cols[i % 2]:
                        render_event_card(event, i)

        st.markdown("---")
        if st.button("📋 Browse All Events", use_container_width=False):
            st.session_state.show_all = True
            st.rerun()

st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.8rem; margin-top:3rem; padding-bottom:2rem;">
  Data sourced from Luma & Eventbrite · Bengaluru, May 2026
</div>
""", unsafe_allow_html=True)