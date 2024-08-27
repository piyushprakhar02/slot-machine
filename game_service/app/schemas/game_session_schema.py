from pydantic import BaseModel, EmailStr


class StartSessionResponse(BaseModel):
    success: bool
    message: str
    allocated_machine_id: str


class SlotMachinePlayResponse(BaseModel):
    success: bool
    slots: list
    message: str
