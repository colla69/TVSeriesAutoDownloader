from src.context import *
import src.tools.conf as cnf
from src.tools.video_downloader import download_videos_todo, check_downloading


todolist = []


if __name__ == '__main__':
    todolist = cnf.load_todo_list()
    download_videos_todo(todolist, cnf.get_out_path())
    check_downloading()

