import threading


# This class is used to manage the correlation of the messages published and consumed with the task sender
class SharedDataHandler:
    _class_instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        self.shared_dict = {}
        self.shared_dict_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._class_instance is None:
                cls._class_instance = super(SharedDataHandler, cls).__new__(cls)

        return cls._class_instance

    def save_origin_did(self, correlation_id, origin_did):
        with self.shared_dict_lock:
            self.shared_dict[correlation_id] = origin_did
        print("saved shared_data: ", self.shared_dict)

    def get_origin_did(self, correlation_id):
        print("get shared_data: ", self.shared_dict)
        with self.shared_dict_lock:
            if correlation_id in self.shared_dict:
                return self.shared_dict[correlation_id]
            else:
                return None

    def remove_origin_did(self, correlation_id):
        with self.shared_dict_lock:
            del self.shared_dict[correlation_id]
        print("removed shared_data: ", self.shared_dict)
