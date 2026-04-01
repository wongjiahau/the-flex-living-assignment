from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/properties")
async def get_properties(
    current_user: dict = Depends(get_current_user)
) -> list[Any]:
    tenant_id = current_user.tenant_id
    
    # Query properties for this tenant from DB
    from app.core.database_pool import DatabasePool
    from sqlalchemy import text
    
    db_pool = DatabasePool()
    await db_pool.initialize()
    
    async with await db_pool.get_session() as session:
        result = await session.execute(
            text("SELECT id, name FROM properties WHERE tenant_id = :tenant_id"),
            {"tenant_id": tenant_id}
        )
        rows = result.fetchall()
    
    return [{"id": row.id, "name": row.name} for row in rows]
