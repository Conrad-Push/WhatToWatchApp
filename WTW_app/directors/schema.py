from pydantic import BaseModel, root_validator


class DirectorModel(BaseModel):
    director_id: int
    name: str

    class Config:
        orm_mode = True
        schema_extra = {"example": {"director_id": 1, "name": "Frank Darabont"}}


class AddDirectorModel(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {"example": {"name": "Elon Musk"}}


class PatchDirectorModel(BaseModel):
    name: str

    @root_validator(pre=True)
    def not_empty(cls, values):
        if not values.get("name"):
            raise ValueError("Name property is required to be not empty!")
        return values

    class Config:
        orm_mode = True
        schema_extra = {"example": {"name": "John Smith"}}
