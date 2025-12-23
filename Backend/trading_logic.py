import logging

# P25-06-04_14-47-51
logger = logging.getLogger(__name__)


def execute_trade(token: str, amount: float, action: str):
    logger.info(f"Executing {action} of {amount} {token}")
