class Constant:
    NUMBER_OF_TOKENS_ON_SIGNUP = 10
    NUMBER_OF_TOKENS_ON_LOGIN = 1

    TOKEN_NEEDED_PER_GAME = 1

    SLOT_MACHINE_STATUS_AVAILABLE = "AVAILABLE"
    SLOT_MACHINE_STATUS_BUSY = "BUSY"
    SLOT_MACHINE_STATUS_BROKEN = "BROKEN"

    INSUFFICIENT_TOKEN_EXCEPTION_MESSAGE = "Insufficient tokens to play game"
    SLOT_MACHINE_UNAVAILABLE_EXCEPTION_MESSAGE = "Slot machines are busy please try again later"

    DEBIT_USER_BALANCE_EXCEPTION_MESSAGE = "Failed to debit token from user"
    CREDIT_SLOT_MACHINE_BALANCE_EXCEPTION_MESSAGE = "Failed to credit balance to the slot machine"

    SLOT_MACHINE_SPIN_EXCEPTION_MESSAGE = "Slot machine did not spin correctly"
