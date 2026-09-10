import streamlit as st

from disease_info import DISEASE_INFO

st.title("📖 Disease Library")
st.write("Browse all 38 crop/disease classes this model was trained to recognize.")

crops = sorted({v["crop"] for v in DISEASE_INFO.values()})
col1, col2 = st.columns([2, 1])
with col1:
    search = st.text_input("Search by crop or condition", placeholder="e.g. tomato, blight, rust...")
with col2:
    crop_filter = st.selectbox("Filter by crop", ["All crops"] + crops)

entries = list(DISEASE_INFO.items())
if crop_filter != "All crops":
    entries = [(k, v) for k, v in entries if v["crop"] == crop_filter]
if search:
    s = search.lower()
    entries = [
        (k, v) for k, v in entries
        if s in v["crop"].lower() or s in v["condition"].lower() or s in k.lower()
    ]

st.caption(f"Showing {len(entries)} of {len(DISEASE_INFO)} classes")
st.divider()

if not entries:
    st.info("No matching diseases. Try a different search term or crop filter.")

for class_name, info in entries:
    is_healthy = "healthy" in class_name.lower()
    tag_class = "healthy-tag" if is_healthy else "disease-tag"
    with st.expander(f"{info['crop']} — {info['condition']}"):
        st.markdown(
            f'<span class="crop-tag">{info["crop"]}</span>'
            f'<span class="crop-tag {tag_class}">{info["condition"]}</span>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(f"**Symptoms:** {info['symptoms']}")
        st.markdown(f"**Likely cause:** {info['causes']}")
        if not is_healthy:
            st.markdown(f"**Treatment / management:** {info['treatment']}")
        else:
            st.markdown(f"**Care tips:** {info['treatment']}")
