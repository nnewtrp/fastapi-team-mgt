from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    teamId: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class TeamUpdate(BaseModel):
    name: str = Field(..., min_length=1)


class Team(BaseModel):
    teamId: str
    name: str
    isDeleted: bool


class TeamResponse(BaseModel):
    data: Team
    isSuccess: bool = True


class TeamListResponse(BaseModel):
    totalItems: int
    data: list[Team]
    isSuccess: bool = True
