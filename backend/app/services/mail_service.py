from sqlalchemy.orm import Session
from ..models import EmailAccount
from ..security import decrypt, encrypt
from imapclient import IMAPClient
import smtplib
import email
import re
from datetime import datetime, timedelta

ATTACHMENT_GROUPS = {
    "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
    "document": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
    "archive": ["zip", "rar", "7z", "tar", "gz"],
    "audio": ["mp3", "wav", "aac", "flac"],
    "video": ["mp4", "mov", "avi", "mkv"],
}


class MailService:

    # ---------- 手动邮箱 ----------
    @staticmethod
    def add_manual_account(user_id: int, data, db: Session):
        acc = EmailAccount(
            user_id=user_id,
            email=data.email,
            provider="manual",
            encrypted_username=encrypt(data.email),
            encrypted_password=encrypt(data.password),
            imap_host=data.imap_host,
            imap_port=data.imap_port,
            imap_ssl=data.imap_ssl,
            smtp_host=data.smtp_host,
            smtp_port=data.smtp_port,
            smtp_ssl=data.smtp_ssl,
        )
        db.add(acc)
        db.commit()
        db.refresh(acc)
        return acc

    @staticmethod
    def test_connection(data):
        # IMAP
        try:
            with IMAPClient(data.imap_host, port=data.imap_port, ssl=data.imap_ssl) as client:
                client.login(data.email, data.password)
        except Exception as e:
            raise Exception(f"IMAP 连接失败：{e}")

        # SMTP
        try:
            if data.smtp_ssl:
                server = smtplib.SMTP_SSL(data.smtp_host, data.smtp_port)
            else:
                server = smtplib.SMTP(data.smtp_host, data.smtp_port)
                server.starttls()
            server.login(data.email, data.password)
            server.quit()
        except Exception as e:
            raise Exception(f"SMTP 连接失败：{e}")

    # ---------- 工具 ----------
    @staticmethod
    def _list_accounts(user_id: int, db: Session):
        return db.query(EmailAccount).filter_by(user_id=user_id).all()

    @staticmethod
    def _build_snippet_from_body(body_raw: bytes) -> str:
        if not body_raw:
            return ""
        try:
            text = body_raw.decode(errors="ignore")
            text = re.sub(r"<[^>]+>", "", text)
            return text.strip().replace("\n", " ")[:100]
        except:
            return ""

    # ---------- 统一收件箱 ----------
    @staticmethod
    def unified_inbox(user_id: int, db: Session):
        accounts = MailService._list_accounts(user_id, db)
        results = []

        for acc in accounts:
            username = decrypt(acc.encrypted_username)
            password = decrypt(acc.encrypted_password)
            try:
                with IMAPClient(acc.imap_host, port=acc.imap_port, ssl=acc.imap_ssl) as client:
                    client.login(username, password)
                    client.select_folder("INBOX")
                    ids = client.search("ALL")[-200:]
                    fetch_data = client.fetch(ids, ["ENVELOPE", "FLAGS", "BODY.PEEK[TEXT]"])
                    for msg_id in ids:
                        env = fetch_data[msg_id][b"ENVELOPE"]
                        flags = fetch_data[msg_id][b"FLAGS"]
                        body_raw = fetch_data[msg_id].get(b"BODY[TEXT]")
                        snippet = MailService._build_snippet_from_body(body_raw)
                        results.append({
                            "account_id": str(acc.id),
                            "account_email": acc.email,
                            "msg_id": msg_id,
                            "subject": env.subject.decode() if env.subject else "(无主题)",
                            "from": f"{env.from_[0].mailbox.decode()}@{env.from_[0].host.decode()}" if env.from_ else "",
                            "date": env.date.isoformat() if env.date else None,
                            "is_read": b"\\Seen" in flags,
                            "starred": b"\\Flagged" in flags,
                            "snippet": snippet,
                        })
            except:
                continue

        results.sort(key=lambda x: x["date"] or "", reverse=True)
        return {"results": results}

    # ---------- 统一搜索 ----------
    @staticmethod
    def unified_search(user_id: int, query: str, db: Session):
        accounts = MailService._list_accounts(user_id, db)
        results = []

        for acc in accounts:
            username = decrypt(acc.encrypted_username)
            password = decrypt(acc.encrypted_password)
            try:
                with IMAPClient(acc.imap_host, port=acc.imap_port, ssl=acc.imap_ssl) as client:
                    client.login(username, password)
                    client.select_folder("INBOX")
                    criteria = ["OR", "OR",
                                f'SUBJECT "{query}"',
                                f'FROM "{query}"',
                                f'TEXT "{query}"']
                    ids = client.search(criteria)
                    fetch_data = client.fetch(ids, ["ENVELOPE", "FLAGS", "BODY.PEEK[TEXT]"])
                    for msg_id in ids:
                        env = fetch_data[msg_id][b"ENVELOPE"]
                        flags = fetch_data[msg_id][b"FLAGS"]
                        body_raw = fetch_data[msg_id].get(b"BODY[TEXT]")
                        snippet = MailService._build_snippet_from_body(body_raw)
                        results.append({
                            "account_id": str(acc.id),
                            "account_email": acc.email,
                            "msg_id": msg_id,
                            "subject": env.subject.decode() if env.subject else "(无主题)",
                            "from": f"{env.from_[0].mailbox.decode()}@{env.from_[0].host.decode()}" if env.from_ else "",
                            "date": env.date.isoformat() if env.date else None,
                            "is_read": b"\\Seen" in flags,
                            "starred": b"\\Flagged" in flags,
                            "snippet": snippet,
                        })
            except:
                continue

        results.sort(key=lambda x: x["date"] or "", reverse=True)
        return {"results": results}

    # ---------- 示例：统一发件人过滤 ----------
    @staticmethod
    def unified_from_filter(user_id: int, query: str, db: Session):
        accounts = MailService._list_accounts(user_id, db)
        results = []

        for acc in accounts:
            username = decrypt(acc.encrypted_username)
            password = decrypt(acc.encrypted_password)
            try:
                with IMAPClient(acc.imap_host, port=acc.imap_port, ssl=acc.imap_ssl) as client:
                    client.login(username, password)
                    client.select_folder("INBOX")
                    ids = client.search([f'FROM "{query}"'])
                    fetch_data = client.fetch(ids, ["ENVELOPE", "FLAGS", "BODY.PEEK[TEXT]"])
                    for msg_id in ids:
                        env = fetch_data[msg_id][b"ENVELOPE"]
                        flags = fetch_data[msg_id][b"FLAGS"]
                        body_raw = fetch_data[msg_id].get(b"BODY[TEXT]")
                        snippet = MailService._build_snippet_from_body(body_raw)
                        results.append({
                            "account_id": str(acc.id),
                            "account_email": acc.email,
                            "msg_id": msg_id,
                            "subject": env.subject.decode() if env.subject else "(无主题)",
                            "from": f"{env.from_[0].mailbox.decode()}@{env.from_[0].host.decode()}" if env.from_ else "",
                            "date": env.date.isoformat() if env.date else None,
                            "is_read": b"\\Seen" in flags,
                            "starred": b"\\Flagged" in flags,
                            "snippet": snippet,
                        })
            except:
                continue

        results.sort(key=lambda x: x["date"] or "", reverse=True)
        return {"results": results}

    # 你可以按这个模式继续扩展：subject/date/size/attachments/attachment-type/priority/label 等
