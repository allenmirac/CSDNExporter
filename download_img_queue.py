import os
import threading
from threading import Thread
from queue import Queue
import subprocess
import requests

class Download_img_queue(object):
    def __init__(self, task_queue, is_win=True, num_workers=5):
        self.task_queue = task_queue
        self.headers = {    # headers是请求头，"User-Agent"、"Accept"等字段可通过谷歌Chrome浏览器查找！
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        self.task_lock = threading.Lock()
        self.num_workers = num_workers
        self.workers = []
        self.is_win = is_win

    def worker(self):
        # print("Worker......")
        while True:
            task = self.task_queue.get()
            # print("Queue get......")
            if task is None:
                break

            url, save_path, is_win = task
            self.download_image(url, save_path, is_win)

            self.task_queue.task_done()

    def download_image(self, url, save_path, is_win):
        # download_cmd = "aria2c --file-allocation=none -c -x 10 -s 10 -o {} {}".format(save_path, url)
        # os.system(download_cmd)
        # print(url, " is downloading......")

        # # 使用aria2
        # if is_win:
        #     download_img_cmd = 'aria2c.exe --file-allocation=none -c -x 10 -s 10 -o {} {}'.format(save_path, url)
        # else:
        #     download_img_cmd = 'aria2c --file-allocation=none -c -x 10 -s 10 -o {} {}'.format(save_path, url)
        # if not os.path.exists(save_path):
        #     subprocess.run(download_img_cmd, shell=True)
        
        # 使用request
        try:
            pic = requests.get(url, headers=self.headers)
            if not os.path.exists(save_path):
                # 如果文件路径不存在，则创建目录
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb+') as f:
                f.write(pic.content)
        except Exception as e:
            print(e)


    def add_task(self, url, save_path, is_win):
        with self.task_lock:
            self.task_queue.put((url, save_path, is_win))

    def start(self):
        for _ in range(self.num_workers):
            t = threading.Thread(target=self.worker)
            t.start()
            self.workers.append(t)

    def stop(self):
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for t in self.workers:
            t.join()

        print("All tasks completed.")
