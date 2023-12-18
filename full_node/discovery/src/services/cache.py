from datetime import timedelta
import redis
from config import Config


# Wrapper class for discovery operations
class DCache:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.cache = redis.Redis(
            host=config.get_redis_host(),
            port=config.get_redis_port(),
            decode_responses=True,
        )
        
    def ping(self) -> bool:
        return self.cache.ping()
    
    def reconnect(self) -> None:
        self.cache = redis.Redis(
            host=self.config.get_redis_host(),
            port=self.config.get_redis_port(),
            decode_responses=True,
        )
        
    def set_result(self, transaction_id: str, value: str) -> None:
        try:
            self.cache.set(transaction_id + "result", value)
            self.cache.expire(transaction_id, timedelta(minutes=60 * 30))
            print(f"Result {transaction_id} saved to cache")
        except Exception as e:
            print(e, "error saving result to cache")
            print(transaction_id, value)
        
    def get_result(self, transaction_id: str) -> str:
        return self.cache.get(transaction_id + "result")

    def delete_result(self, transaction_id: str):
        self.cache.delete(transaction_id + "result")
    
    def set_recipient(self, transaction_id: str, value: str) -> None:
        try:
            self.cache.set(transaction_id + "recipient", value)
            self.cache.expire(transaction_id, timedelta(minutes=60 * 30))
            print(f"Recipient {transaction_id} saved to cache")
        except Exception as e:
            print(e, "error saving recipient to cache")
            print(transaction_id, value)

    def get_recipient(self, transaction_id: str) -> str:
        return self.cache.get(transaction_id + "recipient")

    def delete_recipient(self, transaction_id: str):
        self.cache.delete(transaction_id + "recipient")
