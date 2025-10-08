import asyncio
import time
from fastapi import FastAPI,APIRouter


router = APIRouter()


@router.get("/terrible-ping1")
async def terrible_ping():
    """ A terrible ping endpoint that blocks the event loop"""
    time.sleep(10) # I/O blocking operation for 10 seconds, the whole process will be blocked
    
    return {"pong": True}


@router.get("/terrible-ping2")
async def terrible_ping():
    """ A terrible ping endpoint that blocks the event loop"""
    time.sleep(10) # I/O blocking operation for 10 seconds, the whole process will be blocked
    
    return {"pong": True}

@router.get("/good-ping")
def good_ping():
    """ A good ping endpoint that runs in a separate thread"""
    time.sleep(1) # I/O blocking operation for 1 second, but in a separate thread for the whole `good_ping` route

    return {"pong": True}

@router.get("/perfect-ping1")
async def perfect_ping():
    """ A perfect ping endpoint that uses async/await"""
    await asyncio.sleep(10) # non-blocking I/O operation

    return {"pong": True}

@router.get("/perfect-ping2")
async def perfect_ping():
    """ A perfect ping endpoint that uses async/await"""
    await asyncio.sleep(1) # non-blocking I/O operation

    return {"pong": True}

app = FastAPI()
app.include_router(router)
