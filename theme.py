"""Shared CSS injected on every page for a consistent, polished look."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ---------- Hero banner ---------- */
.hero-banner {
    background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
    border-radius: 1.25rem;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 8px 24px rgba(46, 125, 50, 0.25);
}
.hero-banner h1 {
    color: white !important;
    font-size: 2.4rem;
    margin-bottom: 0.5rem;
}
.hero-banner p {
    color: #E8F5E9 !important;
    font-size: 1.05rem;
    max-width: 640px;
}

/* ---------- Feature / stat cards ---------- */
.feature-card {
    background: white;
    border: 1px solid #E0E0E0;
    border-radius: 1rem;
    padding: 1.25rem;
    height: 100%;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.10);
    border-color: #A5D6A7;
}
.feature-card .icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.feature-card h4 { margin: 0.2rem 0; }
.feature-card p { color: #555; font-size: 0.9rem; margin: 0; }

.stat-box {
    text-align: center;
    background: #F1F8E9;
    border-radius: 1rem;
    padding: 1.1rem 0.5rem;
    border: 1px solid #C8E6C9;
    transition: transform 0.18s ease;
}
.stat-box:hover { transform: translateY(-3px); }
.stat-box .big { font-size: 1.8rem; font-weight: 700; color: #2E7D32; }
.stat-box .label { font-size: 0.8rem; color: #666; }

/* ---------- Result cards (Diagnose page) ---------- */
.result-card {
    padding: 1.25rem 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid #C8E6C9;
    background-color: #F1F8E9;
    margin-bottom: 1rem;
}
.result-card.disease {
    border-color: #FFCC80;
    background-color: #FFF8E1;
}
.confidence-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 1rem;
    background-color: #2E7D32;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
}
.history-item {
    padding: 0.4rem 0.6rem;
    border-radius: 0.5rem;
    background-color: #F1F8E9;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
    transition: background-color 0.15s ease;
}
.history-item:hover { background-color: #DCEDC8; }

/* ---------- Disease library cards ---------- */
.crop-tag {
    display: inline-block;
    padding: 0.1rem 0.55rem;
    border-radius: 1rem;
    background-color: #E8F5E9;
    color: #2E7D32;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.4rem;
}
.healthy-tag { background-color: #E3F2FD; color: #1565C0; }
.disease-tag { background-color: #FFF3E0; color: #E65100; }

/* ---------- Section headers ---------- */
.section-sub { color: #666; margin-top: -0.6rem; margin-bottom: 1.2rem; }
</style>
"""
