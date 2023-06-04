import time
from check_visits_nums import save_valid_links


if __name__ == "__main__":
    start_time = time.time()
    save_valid_links()
    print(f"Время выполнения: {(round(time.time() - start_time, 2)) / 60} минут")