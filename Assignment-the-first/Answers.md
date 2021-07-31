# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz |  |
| 1294_S1_L008_R2_001.fastq.gz |  |
| 1294_S1_L008_R3_001.fastq.gz |  |
| 1294_S1_L008_R4_001.fastq.gz |  |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. ```Your answer here```
    3. ```Your answer here```
    
    2.	What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer.
        - A good quality score cutoff, based on the histograms, is 35 for the index reads and 30 for the biological reads. 
    3.	How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)
        Index 1:
        
        ``` gunzip -c 1294_S1_L008_R2_001.fastq.gz | grep -A1 --no-group-separator '^@K00337' | grep -v '^@K00337' | grep -c 'N' ```

        Out: 3976613
        
        Index 2:
        
        ``` gunzip -c 1294_S1_L008_R3_001.fastq.gz | grep -A1 --no-group-separator '^@K00337' | grep -v '^@K00337' | grep -c 'N'```
        
        Out:3328051    

## Part 2
1. Define the problem 
    - We need to sort the records by index. This is done by comparing the two indexes of each record. If the indexes match then we add the record to the corresponding index bucket. If the indexes don't match we add the record to the swapped_indexes bucket. If the indexes are low quality we add the record to the low_quality bucket.
2. Describe output
    - 52 output files; 24 index files for each of the two reads, a swapped_index file for each of the two reads, and a bad_quality bucket for each of the two reads.
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
