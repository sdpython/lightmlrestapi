"""
@file
@brief Machine Learning Post request
"""
import os
# from filelock import Timeout, FileLock
from .zip_helper import unzip_bytes


class AlreadyExistsException(Exception):
    """
    Exception raised when a project already exists.
    """
    pass


class MLStorage:
    """
    Stores machine learned models into folders.
    """

    def __init__(self, folder):
        """
        @param      folder      folder
        """
        self._folder = folder

    def enumerate_names(self):
        """
        Returns the list of sub folders.
        """
        for root, dirs, _ in os.walk(self._folder):
            for name in dirs:
                desc = os.path.join(root, name, ".desc")
                if os.path.exists(desc):
                    zoo = os.path.relpath(
                        os.path.join(root, name), self._folder)
                    yield zoo.replace("\\", "/")

    def exists(self, name):
        """
        Tells if project *name* exists.

        @param      name        name
        @return                 boolean
        """
        r = os.path.exists(self.get_full_name(name))
        if not r:
            return r
        return os.path.exists(os.path.join(self.get_full_name(name), ".desc"))

    def get_full_name(self, name):
        """
        Returns the full name of a project.

        @param      name        project name
        @return                 full name
        """
        return os.path.join(self._folder, name)

    def _check_name(self, name):
        if name is None or not isinstance(name, str) or len(name) == 0:
            raise ValueError("name cannot be empty.")
        for c in name:
            if "a" <= c <= "z":
                continue
            if "A" <= c <= "Z":
                continue
            if "0" <= c <= "9":
                continue
            if c in '-_./':
                continue
            raise ValueError(
                "A name contains a forbidden character '{0}'".format(name))

    def add(self, name, data):
        """
        Adds a project based on the data.
        A project which already exists cannot be added.

        @param      name        project name, should only contain
                                ascii characters + ``'/'``
        @param      data        dictionary or bytes produced by
                                function @see fn zip_dict
        """
        if not isinstance(data, dict) and not isinstance(data, dict):
            raise TypeError("data should of bytes or a dictionary")
        if isinstance(data, bytes):
            data = unzip_bytes(data)
        self._check_name(name)
        if self.exists(name):
            raise AlreadyExistsException(
                "Project '{0}' already exists.".format(name))
        full = self.get_full_name(name)

        if not os.path.exists(full):
            os.makedirs(full)
        desc = os.path.join(full, ".desc")
        with open(desc, "w") as fd:
            pass

        #lock = FileLock(desc, timeout=2)
        # with lock:
        with open(desc, "a") as fd:
            for k, v in sorted(data.items()):
                subn = "{0}/{1}".format(name, k)
                self._check_name(subn)
                fd.write("{0}\n".format(k))
                n = self.get_full_name(subn)
                with open(n, "wb") as f:
                    f.write(v)

    def get(self, name):
        """
        Retrieves a project based on its name.

        @param      name        project name
        @return                 data
        """
        if not self.exists(name):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        full = self.get_full_name(name)
        desc = os.path.join(full, ".desc")
        if not os.path.exists(desc):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        res = {}
        # lock = FileLock(desc, timeout=1)
        # with lock.acquire():
        with open(desc, "r") as fd:
            lines = fd.readlines()
        for line in lines:
            line = line.strip("\r\n ")
            if line:
                n = os.path.join(full, line)
                with open(n, "rb") as f:
                    res[line] = f.read()
        return res
