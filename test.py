import os
import subprocess
import threading
import time
from queue import Queue

class Aria2Downloader:
    def __init__(self, num_workers=4):
        self.task_queue = Queue()
        self.task_lock = threading.Lock()
        self.workers = []
        self.num_workers = num_workers

    def download_with_aria2(self, url, save_path):
        print(url, " is downloading......")
        download_cmd = ["aria2c", "--file-allocation=none", "-c", "-x", "10", "-s", "10", "-o", save_path, url]
        subprocess.run(download_cmd)
        # print('download_cmd=124')
        # time.sleep(2)

    def worker(self):
        while True:
            task = self.task_queue.get()

            if task is None:
                break

            url, save_path = task

            self.download_with_aria2(url, save_path)
            self.task_queue.task_done()

    def generate_markdown_file(self, url, save_path):
        # 生成 Markdown 文件的逻辑
        # ...
        print("Is downloading......")
        with self.task_lock:
            self.task_queue.put((url, save_path))

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

if __name__ == "__main__":
    downloader = Aria2Downloader(num_workers=10)
    time_start = time.time()
    downloader.start()
    
    # 添加下载任务到队列中，例如：

    downloader.generate_markdown_file('https://img-blog.csdnimg.cn/619d30a6e771448e923644e1936f8032.png#pic_center', './【历史上的今天】7_月_6_日：RSA_算法发明人诞生；AR_游戏_Pokémon_GO_发布；Tumblr_创始人出生\\619d30a6e771448e923644e1936f8032.png')
    downloader.generate_markdown_file('https://img-blog.csdnimg.cn/7a1877cec6c24ae583ce510a35ca0ad5.png#pic_center', './【历史上的今天】7_月_6_日：RSA_算法发明人诞生；AR_游戏_Pokémon_GO_发布；Tumblr_创始人出生\\7a1877cec6c24ae583ce510a35ca0ad5.png')
    downloader.generate_markdown_file('https://img-blog.csdnimg.cn/dad6f05515474de0a6cbcf308f296e19.png#pic_center', './【历史上的今天】7_月_6_日：RSA_算法发明人诞生；AR_游戏_Pokémon_GO_发布；Tumblr_创始人出生\\dad6f05515474de0a6cbcf308f296e19.png')
    downloader.generate_markdown_file('https://img-blog.csdnimg.cn/6d4c26c6949d42ab962bc2815735f991.png', './【历史上的今天】7_月_6_日：RSA_算法发明人诞生；AR_游戏_Pokémon_GO_发布；Tumblr_创始人出生\\6d4c26c6949d42ab962bc2815735f991.png')
    # ...


    # 等待所有任务完成
    downloader.task_queue.join()

    # 停止下载器
    downloader.stop()

    time_end = time.time()
    print("Time Consume:", time_end-time_start)
