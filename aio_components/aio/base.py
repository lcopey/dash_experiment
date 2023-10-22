class BaseAIOId:
    def __init__(self, aio_id: str):
        self.aio_id = aio_id

    def __call__(self, inner_id: str):
        return '-'.join((self.aio_id, inner_id))