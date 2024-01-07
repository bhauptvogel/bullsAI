import numpy as np
import dart
from tqdm import tqdm
import matplotlib.pyplot as plt

def sim_and_plot_diffent_std_values():
    std_values = np.linspace(8.0, 0.1, 500)
    samples = 200000

    print(f"Number of std_values: {len(std_values)}")
    print(f"Number of sim samples per std_value: {samples}")

    indices = np.arange(std_values.size)
    np.random.shuffle(indices)

    std_averages = np.zeros_like(std_values)

    # compute averages
    import concurrent.futures
    import time

    start = time.time()

    def process_index(i):
        print(f'Process {i} started!')
        averages = []
        for _ in range(samples):
            averages.append(dart.leg_sim(std_values[i]))
        std_averages[i] = np.mean(np.array(averages))
        print(f'Process {i} finished!')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_index, i) for i in indices]
        concurrent.futures.wait(futures)

        # averages = []
        # for _ in range(samples):
        #     averages.append(leg_sim_average(std_values[i]))
        # std_averages[i] = np.mean(np.array(averages))

    end = time.time()

    print(f'Finished! Elapsed time: {end-start}')

    dict = {}
    for A, B in zip(std_values, std_averages):
        dict[A] = B
    
    with open(f'sims/sim_{len(std_values)}_{samples}.txt', 'wt') as file:
        file.write(str(dict))

    plt.figure(figsize=(10, 6))
    plt.plot(std_values, np.array(std_averages))
    plt.title('Plot std_values vs averages')
    plt.xlabel('std_values')
    plt.ylabel('averages')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    sim_and_plot_diffent_std_values()