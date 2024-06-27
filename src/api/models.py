from pydantic import BaseModel


class DiscordServer(BaseModel):
    id: int
    name: str
    icon: str
    owner_id: int
    region: str
    member_count: int
    created_at: str
    joined_at: str

    class Config:
        orm_mode = True


class Summoner(BaseModel):
    id: int
    name: str
    tag: str
    profile_icon_id: int
    summoner_level: int
    solo_tier: str
    solo_rank: str
    flex_tier: str
    flex_rank: str

    class Config:
        orm_mode = True

class MatchData(BaseModel):
    team1: list[Summoner]
    team2: list[Summoner]

    class Config:
        orm_mode = True