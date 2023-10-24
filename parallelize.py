import subprocess
import sys

# number of windows
windows = [i for i in range(10)] # to be taken via prior calculation

def parallelize(vcf_path, window_size):

    processes = []

    for window_number in windows:
        command = ['python3', 'vcf_to_hapmap.py', vcf_path, str(window_size), str(window_number)]
        
        # Start a new process for each instance
        process = subprocess.Popen(command)
        processes.append(process)
        
    for process in processes:
        process.wait()
    print('All processes finished')
    
if __name__ == "__main__":
    parallelize(sys.argv[1], sys.argv[2])