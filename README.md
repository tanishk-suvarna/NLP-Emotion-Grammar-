# NLP Grammar & Emotion Analyzer

The Netlify site serves `public/index.html` with its stylesheet from `public/static/`.
`netlify.toml` sets the publish directory explicitly; no frontend build is required.

The Analyze Text button calls `/analyze`, a Node.js Netlify Function. It preserves
the original nine subject–verb agreement correction rules and uses Netlify AI
Gateway with Claude Haiku for emotion and sentiment classification. This replaces
the Flask/PyTorch runtime on Netlify, which does not run a persistent Python web
server. AI inference requires a credit-based Netlify plan with available credits.
Text is processed for analysis and is not stored by this application.

The original `app.py` and `requirements.txt` remain available as a standalone
Flask implementation, but are not part of the deployed site.

For local development, install dependencies with `npm install`, then run
`netlify dev --port 8889`. Use `npm run typecheck` to validate the function types.
