from fastapi import APIRouter, HTTPException, status

from database import teams_collection
from models import Team, TeamCreate, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


def _serialize(doc: dict) -> Team:
    return Team(teamId=doc["teamId"], name=doc["name"], isDeleted=doc["isDeleted"])


@router.get("", response_model=list[Team])
async def list_teams():
    cursor = teams_collection.find({"isDeleted": False})
    return [_serialize(doc) async for doc in cursor]


@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: str):
    doc = await teams_collection.find_one({"teamId": team_id})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return _serialize(doc)


@router.post("", response_model=Team, status_code=status.HTTP_201_CREATED)
async def create_team(payload: TeamCreate):
    if await teams_collection.find_one({"teamId": payload.teamId}) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with teamId '{payload.teamId}' already exists",
        )
    doc = {"teamId": payload.teamId, "name": payload.name, "isDeleted": False}
    await teams_collection.insert_one(doc)
    return _serialize(doc)


@router.put("/{team_id}", response_model=Team)
async def update_team(team_id: str, payload: TeamUpdate):
    result = await teams_collection.find_one_and_update(
        {"teamId": team_id},
        {"$set": {"name": payload.name}},
        return_document=True,
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return _serialize(result)


@router.delete("/{team_id}", response_model=Team)
async def delete_team(team_id: str):
    result = await teams_collection.find_one_and_update(
        {"teamId": team_id, "isDeleted": False},
        {"$set": {"isDeleted": True}},
        return_document=True,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found or already deleted",
        )
    return _serialize(result)


@router.put("/undelete/{team_id}", response_model=Team)
async def undelete_team(team_id: str):
    result = await teams_collection.find_one_and_update(
        {"teamId": team_id, "isDeleted": True},
        {"$set": {"isDeleted": False}},
        return_document=True,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found or not deleted",
        )
    return _serialize(result)
