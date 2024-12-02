import threading
import time


def search_in_files_threading(files, keywords, results, thread_id):
    local_results = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        local_results[keyword].append(file.name)
        except Exception as e:
            print(f"Thread-{thread_id}: Error reading file {file}: {e}")
    results.append(local_results)


def threading_search(file_list, keywords):
    threads = []
    results = []
    num_threads = 4
    files_per_thread = len(file_list) // num_threads

    start_time = time.time()

    for i in range(num_threads):
        start_idx = i * files_per_thread
        end_idx = (i + 1) * files_per_thread if i < num_threads - \
            1 else len(file_list)
        thread = threading.Thread(target=search_in_files_threading, args=(
            file_list[start_idx:end_idx], keywords, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    combined_results = {keyword: [] for keyword in keywords}
    for result in results:
        for keyword in keywords:
            combined_results[keyword].extend(result[keyword])

    print(f"Threading execution time: {time.time() - start_time:.2f} seconds")
    return combined_results
