import os
import shutil


class MecaStore:
    def store(self, bucket: str, key: str, value: str, blockno: int):
        """
        Store a value in the store. with the given key and blockno
        """
        raise NotImplementedError

    def retrieve(self, bucket: str, key: str):
        """
        Retrieve the value stored with the given key
        """
        raise NotImplementedError

    def delete(self, bucket: str, key: str):
        """
        Delete the value stored with the given key
        """
        raise NotImplementedError

    def delete_by_blockno(self, bucket: str, blockno: int):
        """
        Delete all values stored with the given blockno
        """
        raise NotImplementedError

    def list_buckets(self):
        """
        Get all buckets stored in the store
        """
        raise NotImplementedError

    def list_bucket(self, bucket: str):
        """
        Get all keys stored in the bucket
        """
        raise NotImplementedError

    def delete_bucket(self, bucket: str):
        """
        Delete all values stored in the bucket
        """
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

class MecaStoreError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class MecaLocalFsStore(MecaStore):
    def __init__(self, path: str = None):
        super().__init__()
        self.path = path
        if not self.path:
            # use home/.meca/store as default path
            self.path = os.path.expanduser("~/.meca/store")
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        else:
            # clear the directory
            for dir in os.listdir(self.path):
                if (
                    os.path.isdir(f"{self.path}/{dir}")
                    and len(os.listdir(f"{self.path}/{dir}")) == 0
                ):
                    # crashed before writing the message in the directory, so we remove it
                    os.rmdir(f"{self.path}/{dir}")

    def store(self, bucket: str, key: str, value: str, blockno: int):
        # store the value in a file with key as the folder
        # check directory and file exits:
        if not os.path.exists(f"{self.path}/{bucket}"):
            os.makedirs(f"{self.path}/{bucket}")

        if os.path.exists(f"{self.path}/{bucket}/{key}"):
            # empty folders already removed in __init__
            return

        with open(f"{self.path}/{bucket}/{key}/{blockno}", "w") as f:
            f.write(value)

    def retrieve(self, bucket: str, key: str) -> tuple[int, str]:
        # retrieve the value from the file with key as the folder
        # check directory and file exits:
        if not os.path.exists(f"{self.path}/{bucket}/{key}"):
            raise MecaStoreError(f"{key} does not exist")

        files = os.listdir(f"{self.path}/{bucket}/{key}")
        if len(files) > 1:
            raise MecaStoreError(f"{key} has more than one file")
        elif len(files) == 0:
            raise MecaStoreError(f"{key} has no file")

        msg_file = files[0]
        with open(f"{self.path}/{bucket}/{key}/{msg_file}", "r") as f:
            return int(msg_file), f.read()

    def delete(self, bucket: str, key: str):
        # delete the value from the file with key as the folder
        # check directory and file exits:
        if os.path.exists(f"{self.path}/{bucket}/{key}"):
            shutil.rmtree(f"{self.path}/{bucket}/{key}")


    def delete_by_blockno(self, blockno):
        # delete all values with the blockno smaller than the given blockno
        for buckets in os.listdir(self.path):
            for key in os.listdir(f"{self.path}/{buckets}"):
                for file in os.listdir(f"{self.path}/{buckets}/{key}"):
                    if int(file) < blockno:
                        os.remove(f"{self.path}/{buckets}/{key}/{file}")
                if len(os.listdir(f"{self.path}/{buckets}/{key}")) == 0:
                    os.rmdir(f"{self.path}/{buckets}/{key}")

    def list_buckets(self):
        # list all buckets
        return os.listdir(self.path)
    
    def list_bucket(self, bucket: str):
        # list all keys in the bucket
        return os.listdir(f"{self.path}/{bucket}")
    
    def delete_bucket(self, bucket: str):
        # delete the bucket
        if os.path.exists(f"{self.path}/{bucket}"):
          shutil.rmtree(f"{self.path}/{bucket}")

    def close(self):
        pass
