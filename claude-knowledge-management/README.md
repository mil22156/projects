# Claude Knowledge Management

Email-driven personal knowledge capture system. Emails with subject prefix  sent to wwhmiller.claud@gmail.com are automatically parsed, routed to the correct project folder in GitHub, and committed as markdown notes.

## How It Works

1. Script polls Gmail for unread  emails
2. Subject and body are scanned against routing keywords in 
3. Note is committed to the matching project folder in the notes repo
4. Email is marked as read

## Setup

### 1. Google Cloud Project
- Create a project at [console.cloud.google.com](https://console.cloud.google.com)
- Enable the **Gmail API** under APIs & Services → Library
- Create OAuth credentials: APIs & Services → Credentials → Create Credentials → OAuth client ID → Desktop app
- Download  and place it at  (repo root)

### 2. OAuth Consent Screen
- APIs & Services → OAuth consent screen → Audience
- Add your Gmail address as a test user

### 3. First Run (One-Time Auth)
Run from an interactive terminal (not a non-interactive shell):
Requirement already satisfied: certifi==2026.2.25 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 1)) (2026.2.25)
Requirement already satisfied: cffi==2.0.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (2.0.0)
Requirement already satisfied: charset-normalizer==3.4.7 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (3.4.7)
Requirement already satisfied: cryptography==46.0.7 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 4)) (46.0.7)
Requirement already satisfied: google-api-core==2.30.3 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 5)) (2.30.3)
Requirement already satisfied: google-api-python-client==2.194.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 6)) (2.194.0)
Requirement already satisfied: google-auth==2.49.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 7)) (2.49.2)
Requirement already satisfied: google-auth-httplib2==0.3.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 8)) (0.3.1)
Requirement already satisfied: google-auth-oauthlib==1.3.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 9)) (1.3.1)
Requirement already satisfied: googleapis-common-protos==1.74.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 10)) (1.74.0)
Requirement already satisfied: httplib2==0.31.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 11)) (0.31.2)
Requirement already satisfied: idna==3.11 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 12)) (3.11)
Requirement already satisfied: oauthlib==3.3.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 13)) (3.3.1)
Requirement already satisfied: proto-plus==1.27.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 14)) (1.27.2)
Requirement already satisfied: protobuf==7.34.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 15)) (7.34.1)
Requirement already satisfied: pyasn1==0.6.3 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 16)) (0.6.3)
Requirement already satisfied: pyasn1_modules==0.4.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 17)) (0.4.2)
Requirement already satisfied: pycparser==3.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 18)) (3.0)
Requirement already satisfied: PyGithub==2.9.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 19)) (2.9.1)
Requirement already satisfied: PyJWT==2.12.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 20)) (2.12.1)
Requirement already satisfied: PyNaCl==1.6.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 21)) (1.6.2)
Requirement already satisfied: pyparsing==3.3.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 22)) (3.3.2)
Requirement already satisfied: python-dotenv==1.2.2 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 23)) (1.2.2)
Requirement already satisfied: requests==2.33.1 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 24)) (2.33.1)
Requirement already satisfied: requests-oauthlib==2.0.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 25)) (2.0.0)
Requirement already satisfied: typing_extensions==4.15.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 26)) (4.15.0)
Requirement already satisfied: uritemplate==4.2.0 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 27)) (4.2.0)
Requirement already satisfied: urllib3==2.6.3 in ./venv/lib/python3.12/site-packages (from -r requirements.txt (line 28)) (2.6.3)
A browser window will open. Sign in and click Allow. This saves  — all future runs are headless.

### 4. Environment Variables
Create a  file in the repo root:


## Running as a Background Service

### Linux (cron)
[?2004h[?1049h[22;0;0t[1;24r(B[m[4l[?7h[39;49m[?1h=[?1h=[?25l[39;49m(B[m[H[2J[22;34H(B[0;7m[ Reading... ](B[m[22;32H(B[0;7m[ Read 23 lines ](B[m[?12l[?25h[24;1H[?1049l[23;0;0t
[?1l>[?2004l

### macOS (launchd)
Create  with a 15-minute interval pointing to .

## Extending Routing Rules
Edit  — add new projects and keywords. No Python changes needed.



Emails that match no keywords go to  for manual review.

## Dry Run
Test routing without committing or marking emails as read:

