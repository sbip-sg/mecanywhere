import threading


# This class is used to manage the correlation of the messages published and consumed with the task sender
class SharedDataHandler:
    _class_instance = None
    _instance_lock = threading.Lock()
    shared_dict = {}
    shared_dict_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._class_instance is None:
                cls._class_instance = super(SharedDataHandler, cls).__new__(cls)
        return cls._class_instance

    @classmethod
    def save_origin_did(cls, correlation_id, origin_did):
        with cls.shared_dict_lock:
            cls.shared_dict[correlation_id] = origin_did
            print("saved shared_data: ", cls.shared_dict)

    @classmethod
    def get_origin_did(cls, correlation_id):
        with cls.shared_dict_lock:
            print("get shared_data ", correlation_id, ": ", cls.shared_dict)
            if correlation_id in cls.shared_dict:
                return cls.shared_dict[correlation_id]
            else:
                return None

    @classmethod
    def remove_origin_did(cls, correlation_id):
        with cls.shared_dict_lock:
            del cls.shared_dict[correlation_id]
            print("removed shared_data", correlation_id, ": ", cls.shared_dict)
