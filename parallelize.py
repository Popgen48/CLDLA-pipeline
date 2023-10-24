import subprocess
import sys

with open('record_counts.txt', 'r') as text_file:
    line = text_file.readline()
    record_count = int(line.split(':')[1].strip()) if line.split(':')[0].strip() == sys.argv[1] else None

if record_count is None:
    print("Record count not found")
    exit(1)



def parallelize(vcf_path, window_size):
    # number of windows
    windows = [i for i in range(record_count - int(window_size) + 1)] 

    processes = []

    for window_number in windows:
        command = ['python3', 'vcf_to_hapmap.py', vcf_path, str(window_size), str(window_number)]
        
        # Start a new process for each instance
        process = subprocess.Popen(command)
        processes.append(process)
        
    print('Total processes created:', len(processes))
    for process in processes:
        process.wait()
    print('All processes finished')
    
if __name__ == "__main__":
    parallelize(sys.argv[1], sys.argv[2])