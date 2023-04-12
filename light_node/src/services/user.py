class UserRegistrationService:
    def __init__(self):
        self.registered = False

    def is_registered(self) -> bool:
        return self.registered

    def set_is_registered(self, value: bool):
        self.registered = value
