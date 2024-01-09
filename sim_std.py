import numpy as np
import dart
import matplotlib.pyplot as plt
import concurrent.futures
import time
from tqdm import tqdm

def leg_sim(std: float) -> float:
    point_total = 501
    darts_thrown = 0

    while point_total > 0:
        point_total_at_beginning = point_total
        for d in range(3):
            darts_thrown += 1
            coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(point_total, 3-d)), std)
            point_total -= dart.get_points_of_coordinates(coordinates)
            if point_total <= 1:
                if not (point_total == 0 and dart.was_double_hit(coordinates)):
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
    # np.random.seed(1)
    # np.random.shuffle(indices)

    std_averages = np.zeros_like(std_values)

    # compute averages
    start = time.time()

    def process_index(i):
        averages = [leg_sim(std_values[i]) for _ in range(samples)]
        std_averages[i] = np.mean(np.array(averages))
        print(std_values[i], std_averages[i])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_index, i) for i in indices]
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            pass

    end = time.time()

    with open(f'dart_sims/sim_{len(std_values)}_{samples}.txt', 'wt') as file:
        file.write(str({A: B for A, B in zip(std_values, std_averages)}))

    print(f'Finished! Elapsed time: {round(end-start,2)} s \nResults in dart_sims/sim_{len(std_values)}_{samples}.txt')
    
    plt.figure(figsize=(10, 6))
    plt.plot(std_values, np.array(std_averages))
    plt.title('Plot std_values vs averages')
    plt.xlabel('std_values')
    plt.ylabel('averages')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    sim_and_plot_diffent_std_values()
