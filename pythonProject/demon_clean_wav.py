import os
import time


def deamon_clean_wavs():
    deleted_folders_count = 0
    deleted_files_count = 0

    DIR = "static/wavs"
    count_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    print(count_files)
    if count_files > 20:
        if os.path.exists(DIR):
            for root_folder, folders, files in os.walk(DIR):
                for file in files:
                    if file != "test_ruslan.wav":
                        file_path = os.path.join(root_folder, file)
                        # comparing the days
                        remove_file(file_path)
                        deleted_files_count += 1
    hour = 1
    seconds = time.time() - (hour * 60 * 60)

    print(f"Total folders deleted: {deleted_folders_count}")
    print(f"Total files deleted: {deleted_files_count}")


#
# def remove_folder(path):
#     if not shutil.rmtree(path):
#         print(f"{path} is removed successfully")
#     else:
#         print(f"Unable to delete the {path}")


def remove_file(path):
    if not os.remove(path):
        print(f"{path} is removed successfully")
    else:
        print(f"Unable to delete the {path}")


def get_file_or_folder_age(path):
    ctime = os.stat(path).st_ctime
    return ctime


if __name__ == "__main__":
    deamon_clean_wavs()
