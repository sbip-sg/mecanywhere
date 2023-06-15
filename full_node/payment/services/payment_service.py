import aiohttp
import random
import redis
from config import Config
from contract import PaymentContract


class PaymentService:
    def __init__(
        self,
        contract: PaymentContract,
        session: aiohttp.ClientSession,
        redis: redis.Redis,
        config: Config,
    ):
        self.contract = contract
        self.session = session
        self.redis = redis
        self.config = config

    # return random 9 digit decimal
    def _generate_nonce() -> int:
        return random.randint(100000000, 999999999)

    # Adds record of payer address, amount and nonce to db
    async def create_payment_notice(
        self, payer_did: str, payer_addr: str, amount: int
    ) -> int:
        nonce = self._generate_nonce()
        self.contract.set_due(
            nonce,
            payer_did,
            payer_addr,
            amount,
        )
        return nonce

    async def process_payment(self, payer_addr: str, amount: int, nonce: int):
        (nonce, record_did, record_address, record_amount) = self.contract.getDue(nonce)
        if record_address == payer_addr and record_amount == amount:
            print("Payment received successfully")
            self.contract.remove_due(nonce)
            self.contract.increase_balance(record_did, amount)
        else:
            print("Unidentified payment received")
            # TODO: Handle payment failure

    def get_balance(self, did) -> int:
        return self.contract.get_balance(did)
