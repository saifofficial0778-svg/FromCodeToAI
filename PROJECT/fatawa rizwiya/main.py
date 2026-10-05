import fitz  # pip install pymupdf
import streamlit as st

PDF_FILES = {
    "v1_alif": "data/fatawa-razawiyya-jild-1-part-1.pdf",
    # add more volumes here
}

@st.cache_resource
def open_pdf(path: str):
    return fitz.open(path)

@st.cache_data(show_spinner=False)
def render_page(path: str, page_no: int, dpi: int = 130) -> bytes:
    doc = open_pdf(path)
    return doc[page_no - 1].get_pixmap(dpi=dpi).tobytes("png")

def page_viewer(pdf_key: str, start_page: int):
    path = PDF_FILES[pdf_key]
    total = open_pdf(path).page_count
    state_key = f"page_{pdf_key}"

    # Reset to the cited page whenever the user picks a different source
    if st.session_state.get("viewer_src") != (pdf_key, start_page):
        st.session_state["viewer_src"] = (pdf_key, start_page)
        st.session_state[state_key] = start_page

    c1, c2, c3 = st.columns([1, 2, 1])
    if c1.button("◀ Previous"):
        st.session_state[state_key] = max(1, st.session_state[state_key] - 1)
    if c3.button("Next ▶"):
        st.session_state[state_key] = min(total, st.session_state[state_key] + 1)
    c2.markdown(f"**Page {st.session_state[state_key]} / {total}**")

    st.image(render_page(path, st.session_state[state_key]))

# ---------- main app ----------
st.title("Fatawa Razaviyya Search")
query = st.text_input("Ask your question")

if st.button("Search") and query:
    answer, sources = ask(query)            # your existing RAG function
    st.session_state["result"] = (answer, sources)

if "result" in st.session_state:
    answer, sources = st.session_state["result"]
    st.write(answer)
    st.caption("This is a search assistant, not a substitute for a mufti.")

    labels = [f"Vol {s['volume']} · p.{s['pdf_page']}" for s in sources]
    choice = st.radio("Sources", range(len(sources)),
                      format_func=lambda i: labels[i], horizontal=True)
    s = sources[choice]
    page_viewer(s["pdf_key"], s["pdf_page"])