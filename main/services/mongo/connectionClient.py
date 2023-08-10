from mongoengine import connect, disconnect


class ConnectionClient:
    _connection = None

    def __enter__(self) -> None:
        self.open_connection()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_connection()

    @classmethod
    def open_connection(cls) -> bool:
        if not cls._connection:
            cls._connection = connect(
                'auc',
                host='auction-mongo',
                port=27017,
                username='auction-app',
                password='123qwe',
                authentication_source='auc',
                uuidRepresentation="standard"
            )
            return True

        return False

    @classmethod
    def close_connection(cls) -> bool:
        if cls._connection:
            disconnect()
            cls._connection = None
            return True

        return False

    def __del__(self):
        if self._connection:
            disconnect()
