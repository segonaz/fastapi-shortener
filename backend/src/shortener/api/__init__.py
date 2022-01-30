from fastapi import APIRouter

from . import shorten

router = APIRouter()
router.include_router(shorten.router)
