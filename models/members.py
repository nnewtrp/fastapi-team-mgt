from pydantic import BaseModel, Field


class MemberCreate(BaseModel):
    name: str = Field(..., min_length=1)
    teamId: str = Field(..., min_length=1)
    number: int


class MemberUpdate(BaseModel):
    teamId: str = Field(..., min_length=1)
    number: int


class Member(BaseModel):
    name: str
    teamId: str
    number: int


class MemberResponse(BaseModel):
    data: Member
    isSuccess: bool = True


class MemberListResponse(BaseModel):
    totalItems: int
    data: list[Member]
    isSuccess: bool = True
