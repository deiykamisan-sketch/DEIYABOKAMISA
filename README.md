# Lectura AI — Smart Lecture Platform

A graduation-project MVP that combines a digital whiteboard, lecture media, structured notes, transcripts, questions, privacy controls, and secure sharing in one Django application.

## Implemented now

- Account registration, login, logout, authorization, CSRF protection and password hashing.
- Owner-only lecture workspaces with Private/Shared visibility.
- Unpredictable share-token links; private lectures never open through them.
- Lecture video, audio and attachment uploads.
- Transcript, summary and notes stored with the lecture.
- Responsive mouse/touch whiteboard with pen, colors, width, eraser and clear.
- Snapshot storage that preserves the original drawing **and** its recognized-text/diagram-type metadata.
- Questions attached to each lecture.
- Responsive presentation-ready UI and Django admin.
- Automated access-control tests.
- Browser camera and microphone capture in the live classroom.
- WebRTC lecturer-video delivery with database-backed signaling.
- Movable/resizable camera layer over the translucent smart-board stage.
- Composite WebM recording of whiteboard, lecturer video and microphone, uploaded into the lecture record.
- Browser speech-to-text captions in Microsoft Edge and Google Chrome.
- Working Network Architecture diagram button (`PC → Switch → Router → Server`).
- Lecture-code matching with or without a dash and an inline error instead of a 404.

## Camera requirements

Camera, microphone, recording and speech recognition require Microsoft Edge or Google Chrome. Open the site through `http://localhost:8000` or HTTPS and select **Allow** when the browser asks for Camera and Microphone permission. A physical transparent display is not required: the live room simulates it as video, captions and controls layered over a translucent whiteboard.

## Run on Windows, Linux or macOS

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Air writing with an ordinary pen

Put a small bright-green tape or cap near the tip of an ordinary ink pen, stand in front of the laptop camera, then run:

```bash
python run_air_board.py
```

Controls: `Space` enables/disables drawing, `C` clears, and `Q` exits. The desktop window composites the digital ink over your live camera image, producing the virtual transparent-board effect without an electronic pen or physical transparent display. For a phone/IP camera, pass its stream URL:

```bash
python run_air_board.py --camera "http://PHONE_IP:PORT/video"
```

Camera URLs depend on the phone camera application. The laptop's built-in microphone is sufficient for browser recording, speech text, WebRTC and Google Meet.

## Google Meet / OBS

1. Open `run_air_board.py` and confirm that the camera and air writing work.
2. Add the **AI Smart Lecture - Air Board** window as a Window Capture source in OBS Studio.
3. Start **OBS Virtual Camera**.
4. In Google Meet settings, select **OBS Virtual Camera** as the camera and the laptop microphone as the microphone.
5. Run the Django website separately to save lectures, recordings, questions, transcripts and notes.

## Live classroom test

1. Sign in as the lecturer, create a lecture and press **Start live lecture**.
2. Allow camera and microphone access in Edge/Chrome.
3. Copy the displayed lecture code.
4. Open an InPrivate/Incognito window, register a second student account, select **Join by code**, and enter the code. A dash is optional.
5. For testing between different devices, both devices must reach the Django server and browser camera access normally requires HTTPS (localhost is the development exception).

## Test

```bash
python manage.py test
```

## Architecture and extension points

The current version is intentionally modular. Replace the text metadata entry with adapters for OCR/handwriting recognition, speech-to-text and summarization. Camera/phone streaming should enter through a WebRTC service; live whiteboard events through Django Channels/WebSockets. Store large production media in object storage, move SQLite to PostgreSQL, and process AI/media tasks asynchronously with Celery/Redis.

The browser whiteboard remains the source of truth: AI output is always stored beside the original drawing, never over it. This preserves evidence and allows future re-processing with better models.

## Recommended graduation demo flow

1. Create an account and a private Networking lecture.
2. Draw `PC → Switch → Router → Server`, add recognized text, and save the snapshot.
3. Add transcript, summary, notes and media from the lecture form.
4. Add a question and show the complete lecture record.
5. Switch privacy to Shared in admin, copy the link, and open it logged out.
6. Explain the future adapters: camera pen tracking, OCR, STT, summarization, WebRTC and AR display.

## Production hardening still required

Use environment-based secrets, `DEBUG=False`, HTTPS, production hosts, file type/size validation, malware scanning, PostgreSQL, object storage, backups, audit logs, rate limiting and a background job queue before public deployment.
