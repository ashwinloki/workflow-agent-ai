import os

import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

st.set_page_config(
    page_title="Workflow Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLES
# ============================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html,
body,
.stApp {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(221, 214, 254, 0.75),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(207, 250, 254, 0.80),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #ffffff,
            #fafaff 50%,
            #f5fcff
        );

    color: #172033;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ------------------------------------------------------------
   NAVBAR
------------------------------------------------------------ */

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 14px 18px;
    margin-bottom: 60px;

    background: rgba(255, 255, 255, 0.75);

    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 18px;

    box-shadow: 0 12px 40px rgba(79, 70, 229, 0.08);

    backdrop-filter: blur(20px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;

    color: #172033;

    font-size: 17px;
    font-weight: 800;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 36px;
    height: 36px;

    border-radius: 11px;

    background: linear-gradient(
        135deg,
        #8b5cf6,
        #6366f1,
        #06b6d4
    );

    color: #ffffff;

    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.28);
}

.status {
    color: #64748b;

    font-size: 13px;
    font-weight: 500;
}

.status-dot {
    display: inline-block;

    width: 8px;
    height: 8px;

    margin-right: 7px;

    background: #22c55e;

    border-radius: 50%;

    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.13);
}


/* ------------------------------------------------------------
   HERO
------------------------------------------------------------ */

.hero {
    max-width: 850px;

    margin: 0 auto 55px auto;

    text-align: center;
}

.hero-badge {
    display: inline-block;

    padding: 8px 15px;
    margin-bottom: 22px;

    background: rgba(255, 255, 255, 0.80);

    border: 1px solid rgba(124, 58, 237, 0.15);
    border-radius: 100px;

    color: #7c3aed;

    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

.hero-title {
    margin: 0;

    color: #172033;

    font-size: clamp(44px, 6vw, 70px);
    font-weight: 800;

    letter-spacing: -4px;
    line-height: 1.06;
}

.gradient-text {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #6366f1,
        #0891b2
    );

    background-clip: text;
    -webkit-background-clip: text;

    color: transparent;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 650px;

    margin: 23px auto 0 auto;

    color: #64748b;

    font-size: 17px;
    line-height: 1.75;
}


/* ------------------------------------------------------------
   WORKSPACE
------------------------------------------------------------ */

.workspace-label {
    margin-bottom: 7px;

    color: #7c3aed;

    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.workspace-title {
    margin-bottom: 6px;

    color: #172033;

    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
}

.workspace-description {
    margin-bottom: 24px;

    color: #64748b;

    font-size: 14px;
}


/* ------------------------------------------------------------
   INPUT LABELS
------------------------------------------------------------ */

[data-testid="stTextInput"] label p,
[data-testid="stTextArea"] label p {
    color: #344054 !important;

    font-size: 14px !important;
    font-weight: 600 !important;
}


/* ------------------------------------------------------------
   OBJECTIVE INPUT
------------------------------------------------------------ */

[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;

    border: 1px solid #d8dee9 !important;
    border-radius: 14px !important;

    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05) !important;
}

[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: #7c3aed !important;

    box-shadow:
        0 0 0 4px rgba(124, 58, 237, 0.10),
        0 10px 30px rgba(99, 102, 241, 0.08) !important;
}

[data-testid="stTextInput"] input {
    min-height: 52px !important;

    background-color: #ffffff !important;

    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;

    caret-color: #7c3aed !important;

    font-size: 15px !important;

    opacity: 1 !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #667085 !important;
    -webkit-text-fill-color: #667085 !important;

    opacity: 1 !important;
}


/* ------------------------------------------------------------
   SOURCE CONTENT TEXTAREA
------------------------------------------------------------ */

[data-testid="stTextArea"] div[data-baseweb="textarea"] {
    background-color: #ffffff !important;

    border: 1px solid #d8dee9 !important;
    border-radius: 14px !important;

    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05) !important;
}

[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
    border-color: #0891b2 !important;

    box-shadow:
        0 0 0 4px rgba(8, 145, 178, 0.10),
        0 10px 30px rgba(8, 145, 178, 0.08) !important;
}

[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;

    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;

    caret-color: #0891b2 !important;

    font-size: 15px !important;
    line-height: 1.7 !important;

    opacity: 1 !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: #667085 !important;
    -webkit-text-fill-color: #667085 !important;

    opacity: 1 !important;
}


/* ------------------------------------------------------------
   BUTTON
------------------------------------------------------------ */

.stButton > button {
    width: 100%;
    min-height: 54px;

    margin-top: 8px;

    background: linear-gradient(
        100deg,
        #7c3aed,
        #6366f1,
        #0891b2
    );

    border: none;
    border-radius: 14px;

    color: #ffffff !important;

    font-size: 15px;
    font-weight: 700;

    box-shadow: 0 14px 30px rgba(99, 102, 241, 0.24);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    color: #ffffff !important;

    box-shadow: 0 18px 40px rgba(99, 102, 241, 0.32);
}


/* ------------------------------------------------------------
   PROCESS SECTION
------------------------------------------------------------ */

.process {
    margin-top: 60px;
    padding: 30px;

    background: rgba(255, 255, 255, 0.70);

    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 22px;

    box-shadow: 0 18px 60px rgba(71, 85, 105, 0.08);

    text-align: center;

    backdrop-filter: blur(20px);
}

.process-title {
    margin-bottom: 7px;

    color: #172033;

    font-size: 21px;
    font-weight: 700;
}

.process-description {
    margin-bottom: 25px;

    color: #8490a3;

    font-size: 13px;
}

.steps {
    display: flex;
    align-items: center;
    justify-content: center;

    gap: 12px;

    flex-wrap: wrap;
}

.step {
    padding: 11px 16px;

    background: #ffffff;

    border: 1px solid #eaecf0;
    border-radius: 12px;

    color: #475467;

    font-size: 13px;
    font-weight: 600;

    box-shadow: 0 5px 15px rgba(15, 23, 42, 0.04);
}

.step-number {
    margin-right: 7px;

    color: #7c3aed;

    font-weight: 700;
}

.arrow {
    color: #b8c0cc;
}


/* ------------------------------------------------------------
   FEATURE CARDS
------------------------------------------------------------ */

.cards {
    display: grid;

    grid-template-columns: repeat(3, 1fr);

    gap: 15px;

    margin-top: 18px;
}

.card {
    padding: 21px;

    background: rgba(255, 255, 255, 0.72);

    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 17px;

    box-shadow: 0 12px 35px rgba(71, 85, 105, 0.06);

    backdrop-filter: blur(20px);
}

.card-icon {
    margin-bottom: 12px;

    font-size: 20px;
}

.card-title {
    margin-bottom: 7px;

    color: #273247;

    font-size: 14px;
    font-weight: 700;
}

.card-text {
    color: #667085;

    font-size: 12px;
    line-height: 1.6;
}


/* ------------------------------------------------------------
   FOOTER
------------------------------------------------------------ */

.custom-footer {
    margin-top: 65px;

    color: #98a2b3;

    font-size: 12px;

    text-align: center;
}


/* ------------------------------------------------------------
   RESPONSIVE
------------------------------------------------------------ */

@media (max-width: 800px) {

    .cards {
        grid-template-columns: 1fr;
    }

    .hero-title {
        letter-spacing: -2px;
    }

    .arrow {
        display: none;
    }
}


/* ------------------------------------------------------------
   STREAMLIT CLEANUP
------------------------------------------------------------ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* ============================================================
   RESULTS
============================================================ */

.results-header {
    margin-top: 60px;
    margin-bottom: 30px;

    padding: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(237, 233, 254, 0.85),
            rgba(224, 242, 254, 0.85)
        );

    border: 1px solid rgba(124, 58, 237, 0.10);
    border-radius: 20px;

    box-shadow:
        0 14px 40px rgba(99, 102, 241, 0.08);
}


.results-label {
    margin-bottom: 7px;

    color: #16a34a;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1px;
}


.results-title {
    margin-bottom: 7px;

    color: #172033;

    font-size: 25px;
    font-weight: 800;

    letter-spacing: -0.8px;
}


.results-description {
    color: #64748b;

    font-size: 14px;
}


/* ------------------------------------------------------------
   PLAN
------------------------------------------------------------ */

.plan-title,
.output-title {
    margin-top: 28px;
    margin-bottom: 14px;

    color: #172033;

    font-size: 18px;
    font-weight: 750;
}


.task-list {
    display: flex;

    gap: 10px;

    flex-wrap: wrap;

    margin-bottom: 32px;
}


.task-chip {
    display: inline-flex;

    align-items: center;

    gap: 7px;

    padding: 9px 13px;

    background: #ffffff;

    border: 1px solid #e4e7ec;
    border-radius: 100px;

    color: #475467;

    font-size: 13px;
    font-weight: 600;

    box-shadow:
        0 5px 15px rgba(15, 23, 42, 0.04);
}


.task-check {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    width: 19px;
    height: 19px;

    background: #dcfce7;

    border-radius: 50%;

    color: #16a34a;

    font-size: 11px;
    font-weight: 800;
}


/* ------------------------------------------------------------
   STREAMLIT RESULT CONTAINERS
------------------------------------------------------------ */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        rgba(255, 255, 255, 0.82);

    border:
        1px solid rgba(99, 102, 241, 0.10) !important;

    border-radius:
        18px !important;

    box-shadow:
        0 10px 35px rgba(71, 85, 105, 0.06);

    margin-bottom:
        14px;
}


[data-testid="stVerticalBlockBorderWrapper"] h3 {
    color:
        #273247;

    font-size:
        18px;

    font-weight:
        750;
}


[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li {
    color:
        #475467;

    line-height:
        1.75;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    '<div class="navbar">'
    '<div class="brand">'
    '<div class="brand-icon">✦</div>'
    '<div>Workflow Agent</div>'
    '</div>'
    '<div class="status">'
    '<span class="status-dot"></span>'
    'Agent ready'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-badge">✦ AI-NATIVE WORKFLOW AUTOMATION</div>'
    '<div class="hero-title">'
    'From messy updates to<br>'
    '<span class="gradient-text">clear, actionable work.</span>'
    '</div>'
    '<div class="hero-description">'
    'Give the agent an objective and your raw project content. '
    'It understands the goal, plans the right tasks, and executes '
    'the workflow automatically.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# WORKSPACE
# ============================================================

st.markdown(
    '<div class="workspace-label">AGENT WORKSPACE</div>'
    '<div class="workspace-title">What should we accomplish?</div>'
    '<div class="workspace-description">'
    'Describe the outcome you need and provide the source material.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# INPUTS
# ============================================================

objective = st.text_input(
    "Objective",
    placeholder=(
        "Example: Summarize the update, identify risks, "
        "extract action items and draft a follow-up email"
    ),
)

content = st.text_area(
    "Source content",
    placeholder=(
        "Paste meeting notes, project updates, reports, "
        "emails, or other unstructured business content..."
    ),
    height=280,
)

run_button = st.button(
    "✦ Run intelligent workflow",
    type="primary",
)


# ============================================================
# RUN WORKFLOW
# ============================================================

if run_button:

    if not objective.strip():
        st.warning("Please enter an objective.")

    elif not content.strip():
        st.warning("Please provide source content.")

    else:
        payload = {
            "objective": objective,
            "content": content,
        }

        try:
            with st.spinner(
                "Planning and executing your workflow..."
            ):
                response = requests.post(
                    f"{API_URL}/agent/run",
                    json=payload,
                    timeout=120,
                )

            if response.status_code == 200:
                st.session_state["workflow_result"] = response.json()

            else:
                try:
                    error_message = response.json().get(
                        "detail",
                        "Workflow execution failed.",
                    )

                except ValueError:
                    error_message = (
                        "The backend returned an invalid response."
                    )

                st.error(error_message)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend. "
                "Make sure the FastAPI server is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The workflow took too long to complete. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")


# ============================================================
# RESULTS
# ============================================================

if "workflow_result" in st.session_state:

    data = st.session_state["workflow_result"]

    tasks = data.get("tasks", [])
    results = data.get("results", {})

    st.markdown(
        '<div class="results-header">'
        '<div class="results-label">WORKFLOW COMPLETE</div>'
        '<div class="results-title">Your agent finished the workflow</div>'
        '<div class="results-description">'
        'The AI planner created the task plan and completed the selected actions.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # TASK PLAN
    # --------------------------------------------------------

    if tasks:

        st.markdown(
            '<div class="plan-title">Agent Plan</div>',
            unsafe_allow_html=True,
        )

        task_html = '<div class="task-list">'

        for task in tasks:

            display_name = (
                task
                .replace("_", " ")
                .title()
            )

            task_html += (
                '<div class="task-chip">'
                '<span class="task-check">✓</span>'
                f'{display_name}'
                '</div>'
            )

        task_html += '</div>'

        st.markdown(
            task_html,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # RESULT CARDS
    # --------------------------------------------------------

    if results:

        st.markdown(
            '<div class="output-title">Workflow Results</div>',
            unsafe_allow_html=True,
        )

        task_icons = {
            "summarize": "◫",
            "identify_risks": "⚠",
            "action_items": "✓",
            "draft_email": "✉",
            "generate_report": "▤",
        }

        for task_name, result in results.items():

            display_name = (
                task_name
                .replace("_", " ")
                .title()
            )

            icon = task_icons.get(
                task_name,
                "✦",
            )

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {display_name}"
                )

                st.markdown(result)

    # --------------------------------------------------------
    # NEW WORKFLOW BUTTON
    # --------------------------------------------------------

    if st.button(
        "↻ Start new workflow",
        key="new_workflow",
    ):
        del st.session_state["workflow_result"]
        st.rerun()


# ============================================================
# PROCESS
# ============================================================

st.markdown(
    '<div class="process">'
    '<div class="process-title">'
    'One request. A complete AI workflow.'
    '</div>'
    '<div class="process-description">'
    'The planner decides what needs to happen before '
    'the execution layer begins working.'
    '</div>'
    '<div class="steps">'
    '<div class="step">'
    '<span class="step-number">01</span>Understand'
    '</div>'
    '<div class="arrow">→</div>'
    '<div class="step">'
    '<span class="step-number">02</span>Plan'
    '</div>'
    '<div class="arrow">→</div>'
    '<div class="step">'
    '<span class="step-number">03</span>Execute'
    '</div>'
    '<div class="arrow">→</div>'
    '<div class="step">'
    '<span class="step-number">04</span>Deliver'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown(
    '<div class="cards">'

    '<div class="card">'
    '<div class="card-icon">◎</div>'
    '<div class="card-title">Goal-aware planning</div>'
    '<div class="card-text">'
    'The planner interprets the objective and dynamically '
    'selects the right workflow tasks.'
    '</div>'
    '</div>'

    '<div class="card">'
    '<div class="card-icon">⌘</div>'
    '<div class="card-title">Multi-task execution</div>'
    '<div class="card-text">'
    'Summaries, risks, action items, reports and email drafts '
    'can run in one workflow.'
    '</div>'
    '</div>'

    '<div class="card">'
    '<div class="card-icon">◇</div>'
    '<div class="card-title">Structured delivery</div>'
    '<div class="card-text">'
    'Every result is returned as a clear and inspectable '
    'workflow output.'
    '</div>'
    '</div>'

    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="custom-footer">'
    'Workflow Agent AI · Planner–Executor Architecture'
    '</div>',
    unsafe_allow_html=True,
)