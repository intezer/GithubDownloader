# Github Downloader
Find and download files from multiple Github repositories

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

## About us
http://www.theresponder.co
