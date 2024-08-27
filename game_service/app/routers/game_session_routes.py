from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.game_session_schema import StartSessionResponse, SlotMachinePlayResponse
from app.services.game_session_service import GameSessionService, InsufficientTokensError, NoAvailableMachineError, SlotMachineSpinError, DebitBalanceFromUserError, CreditBalanceToSlotMachineError
from app.database import get_db

router = APIRouter()


@router.post('/{user_id}/start-session',
             response_model=StartSessionResponse,
             summary="Start Game Session",
             description="Initiates a new game session for the specified user. Allocates a slot machine and returns the ID of the allocated machine.",
             response_description="Successful response with the allocated slot machine ID and a message indicating successful allocation."
             )
async def prepare_game_session(user_id: str, db: Session = Depends(get_db)):
    game_session_service = GameSessionService(user_id=user_id, db=db)
    try:
        allocated_slot_machine_id = game_session_service.prepare_session()
        return {"success": True, "allocated_machine_id": allocated_slot_machine_id, "message": "Successfully Allocated"}

    except InsufficientTokensError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NoAvailableMachineError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.post('/{user_id}/machine/{slot_machine_id}/play',
             response_model=SlotMachinePlayResponse,
             summary="Play Slot Machine",
             description="Allows the user to play a game on the specified slot machine. Returns the result of the spin and the amount won, if any.",
             response_description="Successful response with the slot machine spin result, including the slots displayed and a message indicating whether the user won the jackpot or not."
             )
async def spin_slot_machine(user_id: str, slot_machine_id: str, db: Session = Depends(get_db)):
    game_session_service = GameSessionService(user_id=user_id, db=db)
    try:
        token, slots = game_session_service.play_game(slot_machine_id=slot_machine_id)
        if token > 0:
            response = {"success": True, "slots": slots, "message": f"Yay! You won the Jackpot worth {token}"}
        else:
            response = {"success": True, "slots": slots, "message": "Better luck next time!"}

        return response

    except InsufficientTokensError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DebitBalanceFromUserError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except CreditBalanceToSlotMachineError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except SlotMachineSpinError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
