from pathlib import Path
from threading_search import threading_search
from multiprocessing_search import multiprocessing_search

if __name__ == "__main__":
    folder_path = Path('./test_files')
    file_list = list(folder_path.glob('*.txt'))

    keywords = ["test", "debug", "error"]

    print("Running threading search...")
    threading_results = threading_search(file_list, keywords)
    print("Threading Results:", threading_results)

    print("\nRunning multiprocessing search...")
    multiprocessing_results = multiprocessing_search(file_list, keywords)
    print("Multiprocessing Results:", multiprocessing_results)
