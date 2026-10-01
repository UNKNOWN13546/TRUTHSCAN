import asyncio
from app.services.case_orchestrator import CaseOrchestrator
from app.services.seal_service import SealService

async def main():
    text = "URGENT SBI: Your KYC is expired. Transfer Rs 25000 now via UPI or account blocked."
    report = await CaseOrchestrator.process_case(text_content=text, claimed_entity="SBI Bank", channel_sender="sbi-alert@gmail.com")
    print(f"CASE_RESULT: ID={report.case_id} | VERDICT={report.overall_verdict}")
    print("ATTACK_STAGES:", [s.stage_name for s in report.attack_chain if s.detected])
    
    doc = b"Engineering Physics Master Examination Question Paper 2026."
    seal = SealService.issue_seal(doc, "National Testing Agency", "Physics 2026")
    v1 = SealService.verify_seal(doc, seal["seal_payload"])
    print("SEAL_ORIGINAL:", v1["verdict"])
    
    modified_doc = b"Engineering Physics Master Examination Question Paper 2026 [LEAKED COPY]."
    v2 = SealService.verify_seal(modified_doc, seal["seal_payload"])
    print("SEAL_MODIFIED:", v2["verdict"])

if __name__ == "__main__":
    asyncio.run(main())
