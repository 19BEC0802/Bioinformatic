import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to run alignment command and measure execution time
def run_alignment(command, description):
    print(f"Running {description}...")
    start_time = time.time()
    process = subprocess.Popen(command, shell=True)
    process.wait()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{description} completed in {execution_time:.2f} seconds.\n")
    return execution_time

# Function to get alignment statistics using SAMtools
def get_alignment_stats(bam_file):
    stats = subprocess.check_output(f"samtools flagstat {bam_file}", shell=True).decode()
    return stats

# Function to extract number of aligned reads from SAMtools stats
def extract_aligned_reads(stats):
    for line in stats.split("\n"):
        if "mapped (" in line:
            return int(line.split()[0])
    return 0

# Run BWA alignment and measure performance
bwa_command = "./bwa_align.sh"
bwa_time = run_alignment(bwa_command, "BWA Alignment")
bwa_stats = get_alignment_stats("bwa_sorted.bam")

# Run NoVoAlign alignment and measure performance
novo_command = "./novo_align.sh"
novo_time = run_alignment(novo_command, "NoVoAlign Alignment")
novo_stats = get_alignment_stats("novo_sorted.bam")

# Extract aligned reads count
bwa_aligned = extract_aligned_reads(bwa_stats)
novo_aligned = extract_aligned_reads(novo_stats)

# Calculate accuracy and error rates (assuming total reads = 1,000,000)
total_reads = 1000000
bwa_accuracy = (bwa_aligned / total_reads) * 100
novo_accuracy = (novo_aligned / total_reads) * 100
bwa_error_rate = 100 - bwa_accuracy
novo_error_rate = 100 - novo_accuracy

# Create a DataFrame to store the results
results = pd.DataFrame({
    'Algorithm': ['BWA', 'NoVoAlign'],
    'Execution Time (s)': [bwa_time, novo_time],
    'Accuracy (%)': [bwa_accuracy, novo_accuracy],
    'Error Rate (%)': [bwa_error_rate, novo_error_rate],
    'Memory Usage (GB)': [4.5, 6.2]  # Example memory usage values
})

# Print the results
print("\nPerformance Metrics:")
print(results)

# Plot Execution Time Comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Algorithm', y='Execution Time (s)', data=results)
plt.title('Execution Time Comparison')
plt.ylabel('Execution Time (s)')
plt.xlabel('Alignment Algorithm')
plt.show()

# Plot Memory Usage Comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Algorithm', y='Memory Usage (GB)', data=results)
plt.title('Memory Usage Comparison')
plt.ylabel('Memory Usage (GB)')
plt.xlabel('Alignment Algorithm')
plt.show()

# Plot Accuracy Comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Algorithm', y='Accuracy (%)', data=results)
plt.title('Accuracy Comparison')
plt.ylabel('Accuracy (%)')
plt.xlabel('Alignment Algorithm')
plt.show()

# Plot Error Rate Comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Algorithm', y='Error Rate (%)', data=results)
plt.title('Error Rate Comparison')
plt.ylabel('Error Rate (%)')
plt.xlabel('Alignment Algorithm')
plt.show()

# Save results to a CSV file
results.to_csv("alignment_comparison_results.csv", index=False)
print("\nResults saved to 'alignment_comparison_results.csv'")
