def send_email(to:str, subject:str, body:str) -> dict:
    # rn i'll just keep a dummy log but yeah in future we can def use a proper one
    return {
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "note": f"hehehe sent the email to {to} HAHAHAHAHAH"
    }