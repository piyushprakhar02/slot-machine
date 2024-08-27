from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import SlotMachine
from constant import Constant


class SlotMachineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_available_machines(self) -> List[SlotMachine]:
        """
        Fetch all available slot machines.
        """
        return self.db.query(SlotMachine).filter(SlotMachine.status == Constant.SLOT_MACHINE_STATUS_AVAILABLE).all()

    def get_machine_by_id(self, slot_machine_id: str) -> Optional[SlotMachine]:
        """
        Fetch a slot machine by its ID.
        """
        return self.db.query(SlotMachine).filter(SlotMachine.id == slot_machine_id).one_or_none()

    def update_machine_status(self, slot_machine_id: str, status: str) -> None:
        """
        Update the status of a slot machine.
        """
        slot_machine = self.db.query(SlotMachine).filter(SlotMachine.id == slot_machine_id).one_or_none()
        if slot_machine:
            slot_machine.status = status
            self.db.commit()

    def update_machine_balance(self, slot_machine_id: str, balance: int) -> None:
        """
        Update the balance of a slot machine.
        """
        slot_machine = self.db.query(SlotMachine).filter(SlotMachine.id == slot_machine_id).one_or_none()
        if slot_machine:
            slot_machine.balance = balance
            self.db.commit()
