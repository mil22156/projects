import os
import yaml
import base64
import re
from datetime import datetime
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from github import Github, Auth

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_gmail_service(credentials_path, token_path):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def fetch_claude_emails(service):
    results = service.users().messages().list(
        userId="me", q="subject:[CLAUDE] is:unread"
    ).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()
        emails.append(detail)
    return emails


def parse_email(message):
    headers = {h["name"]: h["value"] for h in message["payload"]["headers"]}
    subject = headers.get("Subject", "")
    body = _extract_body(message["payload"])
    return {"message_id": message["id"], "subject": subject, "body": body}


def _extract_body(payload):
    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data", "")
        return base64.urlsafe_b64decode(data).decode("utf-8") if data else ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                return base64.urlsafe_b64decode(data).decode("utf-8") if data else ""
    return ""


def route_email(subject, body, routing_rules):
    text = (subject + " " + body).lower()
    for project, rules in routing_rules.items():
        for keyword in rules.get("keywords", []):
            if keyword.lower() in text:
                return project
    return None


def commit_note(repo, project_path, subject, body, dry_run=False):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{project_path}/{timestamp}.md"
    content = f"# {subject}

{body}
"
    commit_message = f"[CLAUDE-INBOX] {datetime.now().strftime("%Y-%m-%d")} — {subject}"

    if dry_run:
        print(f"  [DRY RUN] Would commit: {filename}")
        return

    try:
        existing = repo.get_contents(filename)
        repo.update_file(filename, commit_message, content, existing.sha)
    except Exception:
        repo.create_file(filename, commit_message, content)

    print(f"  Committed: {filename}")


def run(dry_run=False):
    config = load_config()

    gmail = get_gmail_service(
        config["gmail"]["credentials_path"],
        config["gmail"]["token_path"]
    )

    g = Github(auth=Auth.Token(os.environ["GITHUB_TOKEN"]))
    repo = g.get_repo(os.environ.get("NOTES_REPO", "mil22156/claude-notes"))

    emails = fetch_claude_emails(gmail)
    if not emails:
        print("No new [CLAUDE] emails.")
        return

    print(f"Found {len(emails)} email(s).")

    for message in emails:
        email = parse_email(message)
        project = route_email(email["subject"], email["body"], config["routing"])
        folder = f"projects/{project}" if project else "archive"
        print(f"  {email['subject']} → {folder}")

        commit_note(repo, folder, email["subject"], email["body"], dry_run=dry_run)

        if not dry_run:
            gmail.users().messages().modify(
                userId="me", id=email["message_id"],
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
