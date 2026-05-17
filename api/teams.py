from fastapi import APIRouter, HTTPException, Query, status

from database import members_collection, teams_collection
from models.members import MemberSummary
from models.teams import (
    Team,
    TeamCreate,
    TeamDetail,
    TeamDetailResponse,
    TeamListResponse,
    TeamResponse,
    TeamUpdate,
)

router = APIRouter(prefix="/teams", tags=["teams"])


def _serialize(doc: dict) -> Team:
    return Team(teamId=doc["teamId"], name=doc["name"], isDeleted=doc["isDeleted"])


def _serialize_member(doc: dict) -> MemberSummary:
    return MemberSummary(name=doc["name"], number=doc["number"])


@router.get("", response_model=TeamListResponse)
async def list_teams(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
):
    filt = {"isDeleted": False}
    total = await teams_collection.count_documents(filt)
    cursor = teams_collection.find(filt).skip((page - 1) * pageSize).limit(pageSize)
    data = [_serialize(doc) async for doc in cursor]
    return TeamListResponse(totalItems=total, page=page, pageSize=pageSize, data=data)


@router.get("/{team_id}", response_model=TeamDetailResponse)
async def get_team(team_id: str):
    doc = await teams_collection.find_one({"teamId": team_id})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    members = [_serialize_member(m) async for m in members_collection.find({"teamId": team_id})]
    detail = TeamDetail(
        teamId=doc["teamId"],
        name=doc["name"],
        members=members,
        isDeleted=doc["isDeleted"],
    )
    return TeamDetailResponse(data=detail)


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(payload: TeamCreate):
    if await teams_collection.find_one({"teamId": payload.teamId}) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with teamId '{payload.teamId}' already exists",
        )
    doc = {"teamId": payload.teamId, "name": payload.name, "isDeleted": False}
    await teams_collection.insert_one(doc)
    return TeamResponse(data=_serialize(doc))


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: str, payload: TeamUpdate):
    result = await teams_collection.find_one_and_update(
        {"teamId": team_id},
        {"$set": {"name": payload.name}},
        return_document=True,
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return TeamResponse(data=_serialize(result))


@router.delete("/{team_id}", response_model=TeamResponse)
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
    return TeamResponse(data=_serialize(result))


@router.put("/undelete/{team_id}", response_model=TeamResponse)
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
    return TeamResponse(data=_serialize(result))
