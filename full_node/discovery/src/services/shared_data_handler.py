import threading


# This class is used to manage the correlation of the messages published and consumed
class SharedDataHandler:
    _class_instance = None

    def __init__(self):
        self.shared_dict = {}
        self.shared_dict_lock = threading.Lock()

    def __new__(cls):
        if cls._class_instance is None:
            cls._class_instance = super(SharedDataHandler, cls).__new__(cls)
        return cls._class_instance

    def save_origin_did(self, correlation_id, origin_did):
        with self.shared_dict_lock:
            self.shared_dict[correlation_id] = origin_did
        print("shared_data: ", self.shared_dict)

    def get_origin_did(self, correlation_id):
        with self.shared_dict_lock:
            print("shared_data: ", self.shared_dict)
            if correlation_id in self.shared_dict:
                return self.shared_dict[correlation_id]
            else:
                return None

    def remove_origin_did(self, correlation_id):
        with self.shared_dict_lock:
            del self.shared_dict[correlation_id]
        print("shared_data: ", self.shared_dict)
