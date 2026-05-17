from fastapi import APIRouter, HTTPException, status

from database import members_collection, teams_collection
from models.members import (
    Member,
    MemberCreate,
    MemberListResponse,
    MemberResponse,
    MemberUpdate,
)

router = APIRouter(prefix="/members", tags=["members"])


def _serialize(doc: dict) -> Member:
    return Member(name=doc["name"], teamId=doc["teamId"], number=doc["number"])


async def _ensure_team_exists(team_id: str) -> None:
    team = await teams_collection.find_one({"teamId": team_id, "isDeleted": False})
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with teamId '{team_id}' does not exist",
        )


@router.get("", response_model=MemberListResponse)
async def list_members():
    cursor = members_collection.find({})
    data = [_serialize(doc) async for doc in cursor]
    return MemberListResponse(totalItems=len(data), data=data)


@router.get("/{name}", response_model=MemberResponse)
async def get_member(name: str):
    doc = await members_collection.find_one({"name": name})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return MemberResponse(data=_serialize(doc))


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(payload: MemberCreate):
    if await members_collection.find_one({"name": payload.name}) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Member with name '{payload.name}' already exists",
        )
    await _ensure_team_exists(payload.teamId)
    doc = {"name": payload.name, "teamId": payload.teamId, "number": payload.number}
    await members_collection.insert_one(doc)
    return MemberResponse(data=_serialize(doc))


@router.put("/{name}", response_model=MemberResponse)
async def update_member(name: str, payload: MemberUpdate):
    await _ensure_team_exists(payload.teamId)
    result = await members_collection.find_one_and_update(
        {"name": name},
        {"$set": {"teamId": payload.teamId, "number": payload.number}},
        return_document=True,
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return MemberResponse(data=_serialize(result))


@router.delete("/{name}", response_model=MemberResponse)
async def delete_member(name: str):
    result = await members_collection.find_one_and_delete({"name": name})
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return MemberResponse(data=_serialize(result))
