class Cache:
    """
    cache class.
    """

    def __init__(self) -> None:
        """
        Initialization of cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores data and retunrs random key
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
