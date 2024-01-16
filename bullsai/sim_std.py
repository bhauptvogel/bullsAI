import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
import time
from tqdm import tqdm
from bullsai import dart

def leg_sim(std: float) -> float:
    point_total = 501
    darts_thrown = 0

    while point_total > 0:
        point_total_at_beginning = point_total
        darts_thrown += 3
        for d in range(3):
            coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(point_total, 3-d)), std)
            point_total -= dart.get_points_of_coordinates(coordinates)
            if point_total <= 1:
                if point_total == 0 and dart.was_double_hit(coordinates):
                    darts_thrown -= (2-d)
                else:
                    point_total = point_total_at_beginning
                break

    return (501/darts_thrown)*3

def sim_and_plot_diffent_std_values():
    std_values = np.linspace(5.0, 0.1, 500)
    std_values = np.arange(0.1, 5.0, 0.01)
    samples = 100000

    print(f"Number of std_values: {len(std_values)}")
    print(f"Number of sim samples per std_value: {samples}")

    indices = np.arange(std_values.size)

    std_averages = np.zeros_like(std_values)

    # compute averages
    start = time.time()

    LOG_FILE = f'bullsai/dart_sims/sim_{len(std_values)}_{samples}.txt'

    # reset LOG_FILE
    with open(LOG_FILE, 'wt') as file:
        
        file.write('{')

    def process_index(i):
        averages = [leg_sim(std_values[i]) for _ in range(samples)]
        std_averages[i] = np.mean(np.array(averages))
        with open(LOG_FILE, 'at') as file:
            file.write(f'{std_values[i]}: {std_averages[i]},')


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_index, i) for i in indices]
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            pass

    end = time.time()


    with open(LOG_FILE, 'at') as file:
        file.write('}')

    print(f'Finished! Elapsed time: {round(end-start,2)} s \nResults in {LOG_FILE}')
    
    plt.figure(figsize=(10, 6))
    plt.plot(std_values, np.array(std_averages))
    plt.title('Plot std_values vs averages')
    plt.xlabel('std_values')
    plt.ylabel('averages')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    sim_and_plot_diffent_std_values()
