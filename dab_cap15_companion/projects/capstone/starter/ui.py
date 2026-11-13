"""Small Streamlit helpers shared by every page."""
import os

import streamlit as st


def require(key: str, message: str, page: str, label: str):
    """Stop the page with a link to the step that produces `key`, if it has not been done yet."""
    if key not in st.session_state:
        st.info(message)
        st.page_link(page, label=label, icon="➡️")
        st.stop()
    return st.session_state[key]


def secrets_to_environment():
    """On Streamlit Community Cloud, keys live in st.secrets; llm_client reads the environment."""
    try:
        for name in ["LLM_PROVIDER", "LLM_MODEL", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]:
            if name in st.secrets and not os.getenv(name):
                os.environ[name] = str(st.secrets[name])
    except FileNotFoundError:                    # no secrets file: local use with .env, or mock mode
        pass
    except Exception:                            # st.secrets raises its own error when no file exists
        pass
