"""
Shared CSS injected on every page. Uses CSS custom properties (variables) so
light/dark mode can be toggled at runtime via get_css(dark_mode) without a
page reload, and covers both our custom components AND Streamlit's native
widgets (buttons, metrics, expanders, inputs) so the whole page stays
consistent, not just the parts we hand-styled.
"""

LIGHT_VARS = """
:root {
    --bg-color: #FFFFFF;
    --text-color: #1A1A1A;
    --muted-text: #5F6368;
    --card-bg: #FFFFFF;
    --card-border: #E0E0E0;
    --stat-bg: #F1F8E9;
    --stat-border: #C8E6C9;
    --sidebar-bg: #FAFAFA;
    --input-bg: #FFFFFF;
    --accent: #2E7D32;
    --accent-soft: #E8F5E9;
}
"""

DARK_VARS = """
:root {
    --bg-color: #121212;
    --text-color: #F0F0F0;
    --muted-text: #B0B0B0;
    --card-bg: #1E1E1E;
    --card-border: #333333;
    --stat-bg: #16281A;
    --stat-border: #2E7D32;
    --sidebar-bg: #181818;
    --input-bg: #1E1E1E;
    --accent: #66BB6A;
    --accent-soft: #1B2E1B;
}
"""

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* ---------- Base app background / text (covers native widgets too) ---------- */
[data-testid="stAppViewContainer"] { background-color: var(--bg-color); }
[data-testid="stHeader"] { background-color: transparent; }
[data-testid="stSidebar"] { background-color: var(--sidebar-bg); }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
h1, h2, h3, h4, h5, h6, label, .stCaption {
    color: var(--text-color) !important;
}
[data-testid="stMetricValue"] { color: var(--accent) !important; }
[data-testid="stMetricLabel"] { color: var(--muted-text) !important; }
[data-testid="stExpander"] {
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 0.6rem;
}
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: var(--input-bg) !important;
    color: var(--text-color) !important;
}

/* ---------- Hero banner ---------- */
.hero-banner {
    background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
    border-radius: 1.25rem;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 8px 24px rgba(46, 125, 50, 0.25);
    animation: fadeInUp 0.5s ease;
}
.hero-banner h1 { color: white !important; font-size: 2.4rem; margin-bottom: 0.5rem; }
.hero-banner p { color: #E8F5E9 !important; font-size: 1.05rem; max-width: 640px; }

/* ---------- Feature / stat cards ---------- */
.feature-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 1rem;
    padding: 1.25rem;
    height: 100%;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    animation: fadeInUp 0.4s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}
.feature-card .icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.feature-card h4 { margin: 0.2rem 0; color: var(--text-color) !important; }
.feature-card p { color: var(--muted-text) !important; font-size: 0.9rem; margin: 0; }

.stat-box {
    text-align: center;
    background: var(--stat-bg);
    border-radius: 1rem;
    padding: 1.1rem 0.5rem;
    border: 1px solid var(--stat-border);
    transition: transform 0.18s ease;
    animation: fadeInUp 0.4s ease;
}
.stat-box:hover { transform: translateY(-3px); }
.stat-box .big { font-size: 1.8rem; font-weight: 700; color: var(--accent); }
.stat-box .label { font-size: 0.8rem; color: var(--muted-text); }

/* ---------- Result cards (Diagnose page) ---------- */
.result-card {
    padding: 1.25rem 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid var(--stat-border);
    background-color: var(--stat-bg);
    margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease;
}
.result-card.disease { border-color: #FFCC80; background-color: #FFF8E1; }
.result-card h3, .result-card p, .result-card b { color: #1A1A1A !important; }
.confidence-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 1rem;
    background-color: var(--accent);
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
}
.history-item {
    padding: 0.4rem 0.6rem;
    border-radius: 0.5rem;
    background-color: var(--accent-soft);
    color: var(--text-color);
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
    transition: background-color 0.15s ease;
}

/* ---------- Disease library tags ---------- */
.crop-tag {
    display: inline-block;
    padding: 0.1rem 0.55rem;
    border-radius: 1rem;
    background-color: var(--accent-soft);
    color: var(--accent);
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.4rem;
}
.healthy-tag { background-color: #E3F2FD; color: #1565C0; }
.disease-tag { background-color: #FFF3E0; color: #E65100; }

.section-sub { color: var(--muted-text); margin-top: -0.6rem; margin-bottom: 1.2rem; }
</style>
"""


def get_custom_css(dark_mode: bool) -> str:
    vars_css = DARK_VARS if dark_mode else LIGHT_VARS
    return f"<style>{vars_css}</style>" + BASE_CSS