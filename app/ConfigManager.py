
from http import HTTPStatus
import re

from git import Repo
from git.exc import InvalidGitRepositoryError


class ConfigManager(object):

    def __init__(self, log=None):
        self.log = log
        if log is None:
            from defaultLogger import defaultLogger
            self.log = defaultLogger()

        self.decoding_format = 'utf-8'

        # Note: can't use any path, otherwise React/NodeJS will not be able to read
        self.repo_path = 'src/data'
        self.repo = self.getRepo(self.repo_path)

    def getFile(self, source, path_type):
        '''
        Retrieve a schema or configuration file, based on path_type
        '''
        sane = self.pathClean(source)
        if sane is None:
            return HTTPStatus.BAD_REQUEST, "Unable to parse source data name: {source}"

        if path_type == 'data':
            filename = f'{self.repo_path}/{sane}.json'
        else:
            filename = f'src/{path_type}/{sane}.json'

        try:
            with open(filename, 'r') as fd:
                data = fd.read()
        except Exception as ex:
            return HTTPStatus.INTERNAL_SERVER_ERROR, "Unable to read JSON configs: %s" % ex

        return HTTPStatus.OK, data

    def pathClean(self, user_supplied_filename):
        '''
        Basic sanity checking on user-supplied filename
        '''
        try:
            filename = user_supplied_filename.rsplit('/', 1)[-1]
            return re.sub('[^\w]', '', filename)
        except Exception:
            pass

    def saveConfig(self, request, user_supplied_filename, msg='Automated commit'):
        '''
        Save configuration (Flask request object) from the user
        to a configuration file
        '''
        try:
            raw_data = request.json
        except Exception as ex:
            return HTTPStatus.BAD_REQUEST, f"Corrupted JSON message: {ex}"

        if not raw_data:
            return HTTPStatus.BAD_REQUEST, "Empty JSON message"

        saneConfig = self.pathClean(user_supplied_filename)
        filename = f'{self.repo_path}/{saneConfig}.json'
        try:
            configData = request.data.decode(self.decoding_format)
            with open(filename, 'w') as fd:
                fd.write(configData)
            status = dict(config=filename, status="Saved file")
        except Exception as ex:
            self.log.error("Unable to save JSON config", extra=dict(filename=filename, ex_msg=str(ex)))
            return HTTPStatus.INTERNAL_SERVER_ERROR, f"Unable to save JSON config {filename}: {ex}"

        self.addVersion(filename, msg=msg)
        return HTTPStatus.OK, status

    def getRepo(self, path):
        '''
        Use an existing repo, or make a new repo at the path.
        Return None if unable to get a valid repo.
        '''
        try:
            return Repo(path)
        except InvalidGitRepositoryError:
            self.log.info("Not an existing repo", extra=dict(path=path))

        try:
            return Repo.init(path, bare=True)
        except InvalidGitRepositoryError as ex:
            self.log.error("Not able to create repo",
                extra=dict(path=path, ex_msg=ex, traceback=ex.__traceback__))

    def addVersion(self, filenames, msg='Automated commit'):
        '''
        Add a version of a file or files.
        '''
        if self.repo is None:
            return

        if not isinstance(filenames, list):
            filenames = [filenames]

        try:
            self.repo.index.add(filenames)
            self.repo.index.commit(msg)
        except Exception as ex:
            self.log.warning("Not able to version file",
                extra=dict(filenames=filenames, ex_msg=ex, traceback=ex.__traceback__))


if __name__ == '__main__':
    mgr = ConfigManager()


