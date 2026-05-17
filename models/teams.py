from pydantic import BaseModel, Field

from models.members import MemberSummary


class TeamCreate(BaseModel):
    teamId: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class TeamUpdate(BaseModel):
    name: str = Field(..., min_length=1)


class Team(BaseModel):
    teamId: str
    name: str
    isDeleted: bool


class TeamDetail(BaseModel):
    teamId: str
    name: str
    isDeleted: bool
    members: list[MemberSummary]


class TeamResponse(BaseModel):
    data: Team
    isSuccess: bool = True


class TeamDetailResponse(BaseModel):
    data: TeamDetail
    isSuccess: bool = True


class TeamListResponse(BaseModel):
    totalItems: int
    page: int
    pageSize: int
    data: list[Team]
    isSuccess: bool = True
