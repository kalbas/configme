# -*- coding: utf-8 -*-

"""
Asset management.
"""

from io import open as io_open

from os import makedirs

from os.path import basename
from os.path import dirname
from os.path import isdir
from os.path import isfile
from os.path import join

from shutil import rmtree

from .exceptions import AssetCreationError
from .exceptions import AssetLocationTaken
from .exceptions import LocationCreationError
from .exceptions import LocationNotFound
from .exceptions import LocationRemovalError


# --------------------------------------------------------------------------- #
class AssetManager(object):
    """
    Module responsible for asset management such as checking location validity
    creating deleting assets, asset locations and etc.
    """

    # ....................................................................... #
    def location(self, location, location_subject,
                          _os_path_isdir=isdir):
        """

        Return given location first checking if a particular folder path is an
        existing folder. And if not raise a error. Optional message can be
        provided to the error message with regard what kind of path this is.

        :param location: Folder path to check.
        :type location: str/unicode

        :param location_desc: Description of a location to be used in the error
                          message
        :type location_desc: str/unicode

        :return: given location
        :rtype: str/unicode

        :raises: :class:`LocationNotFound` exception if the directory does not
                 exist.
        """

        msg = "%s does not exist, is not a folder, or is not accessible: %s" \
            % (location_subject.capitalize(), location)

        if _os_path_isdir(location) is False:
            raise LocationNotFound(msg)

        return location

    # ....................................................................... #
    def path_join(self, path_parts, _os_path_join=join):
        """
        Join and return the folder path from segments.
        """
        return _os_path_join(*path_parts)

    # ....................................................................... #
    def path_filename(self, path, _os_path_basename=basename):
        """
        Return the file name portion of the given path.

        :param path: full path
        :type path: str/unicode

        :return: file name portion of the given path.
        :type path:
        """
        return _os_path_basename(path)

    # ....................................................................... #
    def path_folder(self, path, _os_path_dirname=dirname):
        """
        Return the file name portion of the given path.

        :param path: full path
        :type path: str/unicode

        :return: file name portion of the given path.
        :type path:
        """
        return _os_path_dirname(path)

    # ....................................................................... #
    def asset_or_location_exists(self, path, _os_path_isfile=isfile):
        """
        Return the file name portion of the given path.

        :param path: full path
        :type path: str/unicode

        :return: file name portion of the given path.
        :type path:
        """

        if _os_path_isfile(path):
            raise AssetLocationTaken(
                "Asset or Location already exist: %s" % path)

        return path

    # ....................................................................... #
    def remove_folder(self, folder_path, _os_path_isdir=isdir,
                      _shutil_rmtree=rmtree):
        """
        Remove folder at the given folder path if it exists.

        :param folder_path: full path of the folder that was removed.
        :type folder_path: str

        :return: folder name
        :rtype: str

        :raises:
            :class:`LocationRemovalError` if folder could not be removed.
        """
        if _os_path_isdir(folder_path):
            try:
                _shutil_rmtree(folder_path)
            except EnvironmentError as err:
                msg = "[Errno %d] %s: '%s'" \
                    % (err.errno, err.strerror, err.filename)
                raise LocationRemovalError(msg)

        return folder_path

    # ....................................................................... #
    def create_folder(self, folder_path, _os_makedirs=makedirs):
        """
        Create folder at the given folder path.

        :param folder_path: full path of the folder that was created.
        :type folder_path: str

        :return: folder name
        :rtype: str

        :raises:

            :class:`LocationCreationError` if folder could not be created.
        """

        try:
            # create the top level folder
            _os_makedirs(folder_path)
        except EnvironmentError as err:
            # someone already created folder, it's OK
            pass

        return folder_path

    # ....................................................................... #
    def write_to_file(self, file_path, content, _io_open=io_open):
        """
        Create file at given file path and write given content to it

        :return: file path of the created file.
        :rtype: str/unicode

        :raises:

            :class:`AssetCreationError` if file could not be created for some
            reason (permssions, or any other file system or os error).
        """
        try:
            file_handler = _io_open(file_path, 'w')
            file_handler.write(content)
            file_handler.close()
        except EnvironmentError as err:
            msg = "[Errno %d] %s: '%s'" \
                % (err.errno, err.strerror, err.filename)
            raise AssetCreationError(msg)

        return file_path
