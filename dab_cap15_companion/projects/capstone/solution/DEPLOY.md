# Deploying to Streamlit Community Cloud

1. Put this folder in its own GitHub repository (it is self-contained: data samples, `requirements.txt`,
   `.streamlit/config.toml`). Check that `.gitignore` lists `.env` and `.streamlit/secrets.toml`, then push.
2. Sign in at share.streamlit.io with GitHub and choose **Create app**. Select the repository, the branch and
   `app.py` as the main file. Choose a subdomain.
3. Open **Advanced settings**. Choose the Python version you tested with (3.12 for this book), and paste the
   contents of your `secrets.toml` into **Secrets**. Leave secrets empty to run in mock mode.
4. Deploy. Watch the build log in **Manage app**; a missing package means a missing line in `requirements.txt`.
5. Open the public URL, run the full flow, and put the URL in your README.
6. Every `git push` to the branch redeploys the app. Rotate a key by editing the Secrets in the app's settings.
