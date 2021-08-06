import time
from posix import listdir
import os
from drive_api_handler import DriveApiHandler


class ChangeLog:
    def __init__(self):
        self.drive_handler = DriveApiHandler()
        self.fileID = None
        self.drive_handler.checkForToken()
        self.checkFileId()
        self.path = None
        self.dir = None

    def setDir(self, new_dir):
        self.dir = new_dir

    def setPath(self, new_path):
        self.path = new_path + self.dir

    def checkFileId(self):
        items = self.drive_handler.getResults()

        if not items:
            self.fileID = self.drive_handler.create()
        else:
            for item in items:
                if item["name"] == "Logs":
                    self.fileID = item["id"]
            if self.fileID == None:
                self.fileID = self.drive_handler.create()

    def printFileId(self):
        print(self.fileID)

    def getFolderLists(self, *, path=None, id=None):
        if path == None:
            path = self.path
        if id == None:
            id = self.fileID
        type = None
        if '.log' not in path and 'bag' not in path:
            folders = dict(local=sorted(os.listdir(path)))
            if len(folders['local']) > 0:
                if 'log' in folders['local'][0] or 'bag' in folders['local'][0]:
                    type = 'file'
                else:
                    type = 'folder'
            if len(folders['local']) == 0:
                return None
            folders['remote'] = sorted(self.drive_handler.getResults(parent=id, type=type),
                                       key=lambda k: k["name"])
            folders['type'] = type
            return folders
        else:
            return None

    def logChangesInFolder(self, *, path=None, id=None):
        if path == None:
            path = self.path
        if id == None:
            id = self.fileID
        folders = self.getFolderLists(path=path, id=id)
        if folders != None:
            if len(folders['remote']) > 0:
                i = 0
                while len(folders['local']) - len(folders['remote']) > 0:
                    while (i >= len(folders['remote']) or folders['local'][i] !=
                           folders['remote'][i]['name']) and i < len(folders['local']):
                        new_file_id = self.drive_handler.create(name=folders['local'][i],
                                                                parents=id,
                                                                type=folders['type'])
                        folders['local'].pop(i)
                    i = i + 1
            else:
                for i in range(0, len(folders['local'])):
                    new_file_id = self.drive_handler.create(name=folders['local'][i],
                                                            parents=id,
                                                            type=folders['type'])
            folders = self.getFolderLists(path=path, id=id)
            for folder in folders['remote']:
                self.logChangesInFolder(path=path + "/" + str(folder['name']), id=folder['id'])
