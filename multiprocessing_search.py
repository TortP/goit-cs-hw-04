import multiprocessing
import time


def search_in_files_multiprocessing(files, keywords, queue):
    local_results = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        local_results[keyword].append(file.name)
        except Exception as e:
            print(f"Process: Error reading file {file}: {e}")
    queue.put(local_results)


def multiprocessing_search(file_list, keywords):
    processes = []
    queue = multiprocessing.Queue()
    num_processes = 4
    files_per_process = len(file_list) // num_processes

    start_time = time.time()

    for i in range(num_processes):
        start_idx = i * files_per_process
        end_idx = (i + 1) * files_per_process if i < num_processes - \
            1 else len(file_list)
        process = multiprocessing.Process(target=search_in_files_multiprocessing, args=(
            file_list[start_idx:end_idx], keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    combined_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword in keywords:
            combined_results[keyword].extend(result[keyword])

    print(f"Multiprocessing execution time: {
          time.time() - start_time:.2f} seconds")
    return combined_results
