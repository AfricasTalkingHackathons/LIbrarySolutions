"""
ArchiveAI – Database Seed Script

Populates the Neon PostgreSQL database with realistic sample data
for testing USSD, SMS, Voice, and Search flows.
"""

import asyncio
from datetime import datetime, timedelta

from app.database import async_session_factory, init_db
import app.models.db_models as db  # noqa: registers tables on Base


async def seed():
    await init_db()

    async with async_session_factory() as session:
        # ── Users ────────────────────────────────────────────────────
        users = [
            db.User(phone_number="+254712345678", language="en"),
            db.User(phone_number="+254798765432", language="sw"),
            db.User(phone_number="+254711223344", language="en"),
            db.User(phone_number="+254700112233", language="ki"),
            db.User(phone_number="+251911234567", language="am"),  # Ethiopia
            db.User(phone_number="+254722334455", language="sw"),
            db.User(phone_number="+254733445566", language="en"),
            db.User(phone_number="+254744556677", language="en"),
        ]
        session.add_all(users)

        # ── SMS Messages ────────────────────────────────────────────
        now = datetime.utcnow()
        sms_messages = [
            db.SMSMessage(
                at_message_id="ATXid_1001",
                phone_number="+254712345678",
                direction="inbound",
                text="colonial land disputes Kenya 1920",
                status="received",
                created_at=now - timedelta(hours=3),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1002",
                phone_number="+254712345678",
                direction="outbound",
                text='ArchiveAI results for "colonial land disputes Kenya 1920":\n\n1. The Kenya Land Commission Report (1933)\n   Analysis of colonial-era land grievances...\n\n2. Crown Lands Ordinance (1915)\n   Legal framework for land allocation...',
                status="sent",
                created_at=now - timedelta(hours=3, minutes=-1),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1003",
                phone_number="+254798765432",
                direction="inbound",
                text="historia ya Mombasa",
                status="received",
                created_at=now - timedelta(hours=2),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1004",
                phone_number="+254798765432",
                direction="outbound",
                text='ArchiveAI matokeo ya "historia ya Mombasa":\n\n1. Mombasa: Mji wa Kale\n   Historia ya bandari ya Mombasa tangu karne ya 11...\n\n2. Fort Jesus na Wareno\n   Ujenzi wa ngome ya Fort Jesus 1593...',
                status="delivered",
                created_at=now - timedelta(hours=2, minutes=-1),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1005",
                phone_number="+254711223344",
                direction="inbound",
                text="Mau Mau detention camps",
                status="received",
                created_at=now - timedelta(hours=1),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1006",
                phone_number="+254711223344",
                direction="outbound",
                text='ArchiveAI results for "Mau Mau detention camps":\n\n1. Pipeline Detention System (1954-1960)\n   British colonial screening and detention...\n\n2. Hola Massacre Report (1959)\n   Official inquiry into detainee deaths...\n\n3. Emergency Regulations (1952)\n   Declaration of state of emergency...',
                status="delivered",
                created_at=now - timedelta(hours=1, minutes=-1),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1007",
                phone_number="+254700112233",
                direction="inbound",
                text="Kikuyu land ownership traditions",
                status="received",
                created_at=now - timedelta(minutes=45),
            ),
            db.SMSMessage(
                at_message_id="ATXid_1008",
                phone_number="+251911234567",
                direction="inbound",
                text="Ethiopian church manuscripts Lalibela",
                status="received",
                created_at=now - timedelta(minutes=30),
            ),
        ]
        session.add_all(sms_messages)

        # ── USSD Sessions ───────────────────────────────────────────
        ussd_sessions = [
            db.USSDSessionRecord(
                session_id="AT_USSD_10001",
                phone_number="+254712345678",
                stage="search_results",
                language="en",
                search_query="colonial land disputes 1920s Kenya",
                search_results=[
                    {"doc_id": "DOC001", "title": "The Kenya Land Commission Report (1933)", "snippet": "Analysis of colonial-era land grievances and recommendations...", "score": 0.94},
                    {"doc_id": "DOC002", "title": "Crown Lands Ordinance (1915)", "snippet": "Legal framework for land allocation in British East Africa...", "score": 0.89},
                    {"doc_id": "DOC003", "title": "Devonshire White Paper (1923)", "snippet": "Declaration of Kenya as primarily African territory...", "score": 0.85},
                ],
                created_at=now - timedelta(hours=2),
            ),
            db.USSDSessionRecord(
                session_id="AT_USSD_10002",
                phone_number="+254798765432",
                stage="main_menu",
                language="sw",
                created_at=now - timedelta(hours=1),
            ),
            db.USSDSessionRecord(
                session_id="AT_USSD_10003",
                phone_number="+254711223344",
                stage="document_detail",
                language="en",
                search_query="independence movement East Africa",
                search_results=[
                    {"doc_id": "DOC010", "title": "Lancaster House Conference (1960)", "snippet": "Negotiations leading to Kenya's independence...", "score": 0.96},
                    {"doc_id": "DOC011", "title": "Kapenguria Six Trial (1952-1953)", "snippet": "Trial of Jomo Kenyatta and five others...", "score": 0.91},
                ],
                created_at=now - timedelta(minutes=30),
            ),
            db.USSDSessionRecord(
                session_id="AT_USSD_10004",
                phone_number="+254722334455",
                stage="confirmation",
                language="sw",
                search_query="vita vya Maji Maji",
                search_results=[
                    {"doc_id": "DOC020", "title": "Maji Maji Rebellion (1905-1907)", "snippet": "Uprising against German colonial rule in Tanganyika...", "score": 0.97},
                ],
                created_at=now - timedelta(minutes=15),
            ),
        ]
        session.add_all(ussd_sessions)

        # ── Voice Recordings ────────────────────────────────────────
        voice_records = [
            db.VoiceRecord(
                session_id="AT_VOICE_5001",
                phone_number="+254712345678",
                recording_url="https://voice.africastalking.com/recordings/5001.wav",
                duration_seconds=12,
                transcription="I am looking for documents about the Kenya land commission from the 1930s",
                language="en",
                created_at=now - timedelta(hours=4),
            ),
            db.VoiceRecord(
                session_id="AT_VOICE_5002",
                phone_number="+254798765432",
                recording_url="https://voice.africastalking.com/recordings/5002.wav",
                duration_seconds=18,
                transcription="Natafuta nyaraka kuhusu historia ya pwani ya Kenya",
                language="sw",
                created_at=now - timedelta(hours=2),
            ),
            db.VoiceRecord(
                session_id="AT_VOICE_5003",
                phone_number="+251911234567",
                recording_url="https://voice.africastalking.com/recordings/5003.wav",
                duration_seconds=8,
                transcription=None,  # transcription pending
                language="am",
                created_at=now - timedelta(minutes=20),
            ),
        ]
        session.add_all(voice_records)

        # ── Search Logs ─────────────────────────────────────────────
        search_logs = [
            db.SearchLog(phone_number="+254712345678", query="colonial land disputes 1920s Kenya", language="en", source="ussd", result_count=3, elapsed_ms=342.5, created_at=now - timedelta(hours=3)),
            db.SearchLog(phone_number="+254712345678", query="colonial land disputes Kenya 1920", language="en", source="sms", result_count=3, elapsed_ms=289.1, created_at=now - timedelta(hours=3)),
            db.SearchLog(phone_number="+254798765432", query="historia ya Mombasa", language="sw", source="sms", result_count=2, elapsed_ms=410.8, created_at=now - timedelta(hours=2)),
            db.SearchLog(phone_number="+254711223344", query="Mau Mau detention camps", language="en", source="sms", result_count=3, elapsed_ms=267.3, created_at=now - timedelta(hours=1)),
            db.SearchLog(phone_number="+254711223344", query="independence movement East Africa", language="en", source="ussd", result_count=2, elapsed_ms=315.6, created_at=now - timedelta(minutes=30)),
            db.SearchLog(phone_number="+254700112233", query="Kikuyu land ownership traditions", language="en", source="sms", result_count=0, elapsed_ms=198.2, created_at=now - timedelta(minutes=45)),
            db.SearchLog(phone_number="+251911234567", query="Ethiopian church manuscripts Lalibela", language="en", source="sms", result_count=4, elapsed_ms=523.1, created_at=now - timedelta(minutes=30)),
            db.SearchLog(phone_number="+254722334455", query="vita vya Maji Maji", language="sw", source="ussd", result_count=1, elapsed_ms=278.9, created_at=now - timedelta(minutes=15)),
            db.SearchLog(phone_number="+254712345678", query="Kenya land commission 1930s", language="en", source="voice", result_count=2, elapsed_ms=445.0, created_at=now - timedelta(hours=4)),
            db.SearchLog(phone_number=None, query="Swahili coast trade routes", language="en", source="api", result_count=5, elapsed_ms=190.4, created_at=now - timedelta(hours=5)),
        ]
        session.add_all(search_logs)

        # ── Document Requests ────────────────────────────────────────
        doc_requests = [
            db.DocumentRequest(
                phone_number="+254712345678",
                doc_id="DOC001",
                doc_title="The Kenya Land Commission Report (1933)",
                status="ready",
                notification_sent=True,
                language="en",
                created_at=now - timedelta(hours=2),
            ),
            db.DocumentRequest(
                phone_number="+254712345678",
                doc_id="DOC002",
                doc_title="Crown Lands Ordinance (1915)",
                status="pending",
                notification_sent=False,
                language="en",
                created_at=now - timedelta(hours=1),
            ),
            db.DocumentRequest(
                phone_number="+254798765432",
                doc_id="DOC015",
                doc_title="Mombasa: Mji wa Kale",
                status="collected",
                notification_sent=True,
                language="sw",
                created_at=now - timedelta(days=1),
            ),
            db.DocumentRequest(
                phone_number="+254711223344",
                doc_id="DOC010",
                doc_title="Lancaster House Conference (1960)",
                status="pending",
                notification_sent=False,
                language="en",
                created_at=now - timedelta(minutes=25),
            ),
            db.DocumentRequest(
                phone_number="+254722334455",
                doc_id="DOC020",
                doc_title="Maji Maji Rebellion (1905-1907)",
                status="pending",
                notification_sent=False,
                language="sw",
                created_at=now - timedelta(minutes=10),
            ),
            db.DocumentRequest(
                phone_number="+251911234567",
                doc_id="DOC030",
                doc_title="Lalibela Rock-Hewn Churches Manuscript Collection",
                status="pending",
                notification_sent=False,
                language="am",
                created_at=now - timedelta(minutes=20),
            ),
        ]
        session.add_all(doc_requests)

        await session.commit()
        print("Seed data inserted successfully!")
        print(f"  Users:             {len(users)}")
        print(f"  SMS Messages:      {len(sms_messages)}")
        print(f"  USSD Sessions:     {len(ussd_sessions)}")
        print(f"  Voice Recordings:  {len(voice_records)}")
        print(f"  Search Logs:       {len(search_logs)}")
        print(f"  Document Requests: {len(doc_requests)}")


if __name__ == "__main__":
    asyncio.run(seed())
