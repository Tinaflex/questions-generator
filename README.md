# 🤖 Startocode Project - Brain Power Question Generator 🚀

Ever wanted to create your own super-powered quiz? This app lets you pick a subject and a topic, and then it finds cool questions for you!

## 📝 Project Overview

This is a fun, web-based quiz tool built for kids! It connects to the Startocode AI API to instantly generate custom study and trivia questions based on any subject and topic you type in.

## 🛠️ Steps / Approach

1. **The Brain (FastAPI):** Set up a Python backend using FastAPI to handle the form fields when you click generate.
2. **The Magic Call (API):** Used the `requests` library to send your specific quiz instructions straight to the Startocode AI endpoint.
3. **The Puzzle Solver (JSON Parsing):** Took the AI's response, parsed it cleanly using `json.loads()`, and looped through the list to build an ordered HTML list (`<ol>`).
4. **The Face Injection:** Opened `static/index.html` and swapped out your custom `` placeholder with your shiny new questions card!

## 🌟 Future Improvements

1. **Error Shield:** Add a friendly fallback message in case the AI API runs out of credits or times out.
2. **Copy Button:** Add a quick "Copy to Clipboard" button next to each generated question for easy sharing.
3. **Save to File:** Add an option to download the final question list as a text file so you can keep it forever.

Built with ❤️ by Faustina Adekpui.