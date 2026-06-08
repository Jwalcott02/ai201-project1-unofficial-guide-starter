import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

css = """
body, .gradio-container, #root, .main, .wrap {
    background-color: #f4f4f4 !important;
    color: #111111 !important;
}
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    font-family: 'Georgia', serif;
}
#header {
    background-color: #003366;
    padding: 20px 30px;
    border-radius: 8px;
    margin-bottom: 16px;
}
#ask-btn {
    background-color: #CC0000 !important;
    color: white !important;
    border: none !important;
    font-size: 1em !important;
    border-radius: 4px !important;
}
#ask-btn:hover {
    background-color: #990000 !important;
}
#answer-box textarea {
    border: 2px solid #003366 !important;
    background-color: white !important;
    color: #111111 !important;
}
#sources-box textarea {
    border: 2px solid #CC0000 !important;
    background-color: white !important;
    color: #003366 !important;
}
"""

with gr.Blocks(css=css, title="FAU CS Unofficial Guide", theme=gr.themes.Default()) as demo:
    with gr.Column(elem_id="header"):
        gr.HTML("""
            <h1 style='color:white; margin:0; font-size:1.8em;'>🦉 FAU CS Unofficial Guide</h1>
            <p style='color:#CC0000; margin:5px 0 0 0; font-style:italic;'>The real knowledge — what students actually say about professors and courses.</p>
        """)

    gr.Markdown("### Ask anything about FAU CS professors, courses, or degree requirements.")

    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. What are the prerequisites for COT4400 Algorithms?",
            scale=4
        )
        btn = gr.Button("Ask", elem_id="ask-btn", scale=1)

    answer = gr.Textbox(
        label="Answer",
        lines=8,
        elem_id="answer-box"
    )

    sources = gr.Textbox(
        label="📄 Retrieved From",
        lines=3,
        elem_id="sources-box"
    )

    gr.Markdown("*Answers are grounded in student reviews and official FAU CS documents. Always verify with your advisor.*")

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()