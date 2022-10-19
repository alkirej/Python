"""
    Author:  Jeff Alkire
    Date:    October 8, 2022
    Purpose: Ensure every Dodger game on the media server contains a poster image that
                is the same (and does not give away the game's winner).
"""
import os
import shutil

POSTER_FILENAME = "poster.jpg"
POSTER_EXTENSION = ".jpg"

def read_dir_list( filename: str ) -> [str]:
    """
    Read the text file containing the directory names this utility should
    process.

    :param filename: the name of the file containing a list of directories
                        containing Dodger games.
    :return: a list of directory names
    """
    with open(filename) as f:
        all_lines = f.readlines()

    return_val = []
    for line in all_lines:
        return_val.append( line.strip() )

    return return_val

def is_video( filename: str ) -> bool:
    """
    Is the given filename a video?  Videos end in .mkv or .mp4.

    :param filename: filename to check
    :return:  True if we have a video, False if not.
    """
    ext = filename[-4:]
    return ext==".mkv" or ext==".mp4"

def is_image( filename: str) -> bool:
    """
    Is the given filename a potential poster image?  Poster images end in .jpg

    :param filename: filename to check
    :return:  True if we have a .jpg file, False if not.
    """
    return filename[-4:]==".jpg"

def strip_ext( filename: str ) -> str:
    """
    Given a filename, remove the extension and return the rest of the filename.

    :param filename: filename needing the extension removed.
    :return: the filename without an extension.
    """
    dot_loc = filename.rfind(".")
    return filename[0:dot_loc]

def read_dir_videos_and_images( dir_name: str ) -> ([str],[str]):
    """
    Look at each file in a given directory.  Return 2 lists.  The first
    containing files expected to be video files and the second with
    the names of files expected to be images/posters.

    :param dir_name: Directory to read filenames from.
    :return: a 2-tuple containing 2 lists of strings.  The first are the
                filenames of videos and the second is the filenames of
                images.  Note, the extensions will have been stripped from
                all the filenames.
    """
    videos = []
    images = []

    files = os.listdir( dir_name )
    # loop through each file in the directory
    for f in files:
        # add images to the correct list
        if is_image(f):
            images.append( strip_ext(f) )
        # add videos to the correct list
        elif is_video(f):
            videos.append( strip_ext(f) )

    return (videos,images)

def log_add_poster( poster_filename: str ) -> None:
    """
    Record our file copy event.

    :param poster_filename: The newly created filename.
    """
    print( "Adding new poster file: " + poster_filename )

def add_poster( dir_name: str, video_name: str ) -> None:
    """
    Add a poster in the given dir with the given name.  The supplied video name
    should not include an extension so this routine can easily add the correct
    extension.

    :param dir_name: Directory the poster should be stored in
    :param video_name: The file name of the poster.
    """
    new_filename = dir_name + os.sep + video_name + POSTER_EXTENSION
    log_add_poster( new_filename )
    shutil.copyfile(POSTER_FILENAME, new_filename )

def process_dir( dir_name: str ) -> None:
    """
    Process one season/directory of dodger games by adding missing poster files.

    :param dir_name: Directory name of one dodger seasonb
    """
    (videos,images) = read_dir_videos_and_images( dir_name )
    for video in videos:
        if not video in images:
            add_poster( dir_name, video )

def main() -> None:
    """
    Read the directories containing Dodger seasons and process them one
    at a time by adding missing poster images.
    """
    directories = read_dir_list("directories.txt")
    for dir in directories:
        process_dir(dir)

if __name__ == "__main__":
    main()
