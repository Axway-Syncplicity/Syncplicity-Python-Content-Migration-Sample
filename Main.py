#!/usr/bin/python3

from Services.UserAPIsClass import ClassUserAPIs
import os
import sys
import platform
import urllib.parse
from Services.AuthenticationClass import Authentication
from Services.FileFolderMetadataClass import FileFolderMetadataClass
from Services.UploadFileClass import Upload
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Content Migration API Options')
    parser.add_argument('-s', '--syncpoint', dest='syncpoint', action='store', required=True,
                        help='enter syncpoint name')
    parser.add_argument('-f', '--folder', dest='folder', action='store', required=True, default='',
                        help='enter path to the local folder to be migrated to Syncplicity')
    parser.add_argument('--as-user', dest='as_user', action='store', required=False, default='',
                        help='enter user email in order to commit in name of a certain user')
    parser.add_argument('--create-syncpoint', dest='create_sp', action='store_true', required=False,
                        help='create syncpoint using the entered syncpoint name and upload content of chosen'
                             ' folder under created syncpoint')
    parser.add_argument('--just-content', dest='just_content', action='store_true', required=False,
                        help='migrate only the content under the specified top level folder (in folder flag)')
    return parser.parse_args()

def __build_file_list(start_path):
    file_list = {}
    index = 1
    for path, _, files in os.walk(start_path):
        for filename in files:
            file_list['file%s' % index] = {
                'filename': filename,
                'filepath': path
            }

            index += 1

    return file_list

def __calculate_upload_filepath_query_parameter(top_folder_name, file_path_relative_to_syncpoint, filename, os_path_separator, just_content):
    syncplicity_separator = '\\'
    relative_path_with_normalized_separator = file_path_relative_to_syncpoint.replace(os_path_separator, syncplicity_separator)
    if just_content:
        syncpoint_path = relative_path_with_normalized_separator
    else:
        syncpoint_path = top_folder_name + relative_path_with_normalized_separator

    full_file_path = syncpoint_path + syncplicity_separator + filename

    # Apply percent-encoding. Separators should also be encoded because this will be a single query parameter value
    return urllib.parse.quote(full_file_path, safe='')

def Main():
    args = parse_args()

    start_path = args.folder
    Credentials = Authentication()
    User_ID = ''
    if args.as_user != '':
        User_ID = ClassUserAPIs(Credentials).GetUser(args.as_user)['Id']
        if User_ID is None:
            sys.exit('could not find such user, exiting')

    if platform.system() == 'Windows':
        os_path_separator = '\\'
        top_folder_name = start_path.split(os_path_separator)[-1]
    else:
        os_path_separator = '/'
        top_folder_name = start_path.split(os_path_separator)[-2]

    syncpoint_class = FileFolderMetadataClass(Credentials, AsUser=User_ID)
    if args.create_sp:
        print('Checking if Syncpoint exists...')
        check_if_sp_exists = syncpoint_class.GetSyncpoint(args.syncpoint)
        if check_if_sp_exists is None:
            print('Syncpoint does not exist, creating Syncpoint...')
            new_sp = syncpoint_class.CreateSyncpoint(args.syncpoint)
            Syncpoint_ID = new_sp[0]['Id']
            Storage_Endpoint_ID = new_sp[0]['StorageEndpointId']
        else:
            print('Syncpoint already exists, continuing using specified Syncpoint')
            Syncpoint_ID = check_if_sp_exists['Id']
            Storage_Endpoint_ID = check_if_sp_exists['StorageEndpointId']
    else:
        Syncpoint = syncpoint_class.GetSyncpoint(args.syncpoint)
        Syncpoint_ID = Syncpoint['Id']
        Storage_Endpoint_ID = Syncpoint['StorageEndpointId']
        if Syncpoint_ID is None:
            sys.exit('No such Syncpoint, exiting')

    storage_endpoint_url = syncpoint_class.get_storage_endpoint_url(Storage_Endpoint_ID)

    file_list = __build_file_list(start_path)

    for file in file_list:
        filename = file_list[file]['filename']
        filepath = file_list[file]['filepath']
        file_path_relative_to_syncpoint = str(filepath.split(top_folder_name, 1)[1])

        syncpoint_path = __calculate_upload_filepath_query_parameter(top_folder_name, file_path_relative_to_syncpoint, filename, os_path_separator, args.just_content)

        UploadFile = Upload(
            Credentials, AsUser=User_ID, filename=filename, full_path=filepath
        ).Upload(Syncpoint_ID, syncpoint_path, storage_endpoint_url)

        # NOTE: upload should be considered successful only if request status code is 200
        # However, there is currently a known issue when uploading a file to a Storage Vault into a non-existent subfolder
        # causes HTTP 500 error. Therefore, for now the sample code considers HTTP 500 to be successful result.
        is_successful_upload = (UploadFile.status_code == 200) or (UploadFile.status_code == 500)

        if is_successful_upload == True:
            print('Successfully uploaded %s' % filename)
        else:
            print('Uploading %s failed (%d)' % (filename, UploadFile.status_code))

Main()
