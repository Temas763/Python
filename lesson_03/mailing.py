from address import address


class mailing:
    def __init__(
        self,
        to_address: address,
        from_address: address,
        cost,
        track
    ):
        self.to_address = to_address
        self.from_address = from_address
        self.cost = cost
        self.track = track
