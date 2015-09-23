# Github Downloader
Find and download files using wildcards from multiple Github repositories

## Requirements
    pip install PyGithub

## Usage
    git_downloader.py [-h] [-r REPO_FILE] [-w WILDCARD] [-o OUTPUT_DIR]
                             [-t TIMEOUT] [-v]
    
    Github file downloader
    
    optional arguments:
      -h, --help            show this help message and exit
      -r REPO_FILE, --repo_file REPO_FILE
                            Path for the input file which contains a url of a
                            Github repository for each separate line
      -w WILDCARD, --wildcard WILDCARD
                            Unix shell-style wildcard to match files to download
                            (for example: *.txt)
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Directory to store all downloaded files
      -t TIMEOUT, --timeout TIMEOUT
                            Socket timeout (seconds)
      -v, --verbose         increase output verbosity
      
## Example
    python git_downloader.py -r repos.txt -w *.txt -o /directory/for/downloaded/files
    
Keep in mind you need to change "repos.txt" to add the repos you want to download from, by adding a Github repository link in each line.
    
## Use to download YARA signatures
This tool can be used to easily download all the YARA signatures in Github.  The example "repos.txt" contains many links to Github repos with YARA signatures, so the only thing left to do is to run the tool with this command:
    python git_downloader.py -r repos.txt -w *.yar* -o /directory/for/downloaded/files
