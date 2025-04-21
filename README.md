# Klix: A Twilio-Based Conversational AI Call Bot
A command line tool that initiates a conversational AI call bot using Twilio for call handling, Deepgram for speech-to-text,OpenAI for natural language understanding, and  Cartesia for text-to-speech.  The bot is designed to engage in natural-sounding conversations with callers, fulfilling user defined use cases ( currently used for screening potential clinical trial participants).

## Features
* **Inbound/Outbound Call Handling:** Uses Twilio to manage inbound and outbound calls.
* **Speech-to-Text (STT):** Converts caller's speech to text using Deepgram.
* **Natural Language Understanding (NLU):** Processes the transcribed text using OpenAI's GPT-4o model.
* **Text-to-Speech (TTS):** Converts bot's responses to speech using Cartesia TTS.
* **Voice Activity Detection (VAD):**  Uses Silero VAD to optimize audio processing.
* **Real-time Conversation:** Maintains context across the conversation.
* **Audio Recording:** Records the entire call for later review.

## Configuration
1. **`.env`:** 
- Copy the example `.example.env` file provided to create a `.env`' file
```bash
cp env.example .env
```
- Fill out the following environment variables:

    * `OPENAI_API_KEY`: Your OpenAI API key.
    * `CARTESIA_API_KEY`: Your Cartesia API key.
    * `DEEPGRAM_API_KEY`: Your Deepgram API key.
    * `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
    * `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
    * `TWILIO_PHONE_NUMBER`: Your Twilio phone number.



2. **`ngrok`:** 
- Install ngrok: Follow the instructions on the [ngrok website](https://download.ngrok.com) to download and install ngrok
- Once installed, in a new terminal, start ngrok to tunnel the local server:

```bash
ngrok http 8765 --subdomain <your_subdomain>
```

Replace `<your_subdomain>` with a unique subdomain.


3. **`Twilio`:**
- Create a Twilio account at [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).
- Access your Twilio phone number's configuration page.
- Under "Voice Configuration", in the "A call comes in" section:
    * Select "Webhook" from the dropdown.
    * Enter your ngrok URL (e.g., `http://<your_subdomain>.ngrok.io`).
    * Ensure "HTTP POST" is selected.
- Click "Save configuration" at the bottom of the page.


4. **`streams.xml`:**
- Copy the template file:

```bash
cp templates/streams.xml.template templates/streams.xml
```

- In `templates/streams.xml`, replace `"wss://your-ngrok-url.ngrok.io/ws"` with your ngrok URL (without `https://`).  The final URL should resemble: `wss://<your_subdomain>.ngrok.io/ws`.

## Usage
This project consists of three main components:

1. **`server.py`:** The FastAPI server that handles WebSocket communication with Twilio and runs the bot logic.

**To run the server:**

```bash
uvicorn server:app --reload
```

2. **`bot.py`:** Contains the core bot logic, including pipeline management and integration with various AI services.

3. **`caller.py`:** A command-line tool to initiate outbound calls using the Twilio API.
 
**To make an outbound call (using the caller.py script):**

```bash
python caller.py +12345678910 --url myapp.ngrok.io
```

Replace `+12345678910` with the desired phone number and `myapp.ngrok.io` with your ngrok url.  Ensure that your `.env` file is correctly configured (see Configuration section).  You may need to adjust the webhook URL in `templates/streams.xml`  to reflect your deployment environment (e.g., if using ngrok).

## Installation
1. Clone the repository:  `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up variables in the Configuration section.
4. Run the ngrok, server and caller script as described above.

## Technologies Used
* **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.  Used for creating the WebSocket server.
* **Pipecat-ai:** A modular pipeline framework for building AI applications, providing components for audio processing, language models, and more.
* **Twilio:** A cloud communications platform used for handling calls.
* **OpenAI:** Provides the large language model (GPT-4o) for natural language understanding.
* **Deepgram:** Provides the Speech-to-Text service.
* **Cartesia:** Provides the Text-to-Speech service.
* **Silero VAD:**  A Voice Activity Detection library.
* **Python (3.7+):** The programming language used for the entire project.
* **Loguru:**  A powerful and user-friendly logging library.
* **Aiofiles:** Asynchronous file I/O library.
* **Uvicorn:** ASGI server implementation for running the FastAPI application.
* **python-dotenv:** For securely managing environment variables.

## Configuration
Create a `.env` file in the project's root directory with the following environment variables:

* `OPENAI_API_KEY`: Your OpenAI API key.
* `CARTESIA_API_KEY`: Your Cartesia API key.
* `DEEPGRAM_API_KEY`: Your Deepgram API key.
* `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
* `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
* `TWILIO_PHONE_NUMBER`: Your Twilio phone number.

## API Documentation
The API is primarily based on WebSockets for real-time communication with Twilio.  The `/twiml` endpoint returns a TwiML response instructing Twilio to connect the call to the WebSocket.

## Dependencies
The project's dependencies are listed in `requirements.txt`.

*README.md was made with [Etchr](https://etchr.dev)*