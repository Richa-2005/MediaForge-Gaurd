from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def get_status():
    return {
        "service": "backend",
        "status": "running",
        "ai_contract": "ready_for_partner_a_stubs",
    }