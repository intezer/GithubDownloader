#!/usr/bin/env python
#

import argparse
import fnmatch
import logging
import os
import posixpath
import socket

try:
    import urlparse
    from urllib import urlretrieve
except ImportError:
    import urllib.parse as urlparse
    from urllib.request import urlretrieve

from github import Github


def main(args_, log_level_):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level_)

    socket.setdefaulttimeout(args_.timeout)

    g = Github()
    with open(args_.repo_file, 'r') as f:
        file_counter = 0
        for line in f.readlines():
            logging.info('Fetching repository: %s' % line)
            try:
                repo_str = line.rstrip().split('github.com/')[-1]
                repo = g.get_repo(repo_str)
                tree = repo.get_git_tree('master', recursive=True)
                files_to_download = []
                for file in tree.tree:
                    if fnmatch.fnmatch(file.path, args_.wildcard):
                        files_to_download.append('https://github.com/%s/raw/master/%s' % (repo_str, file.path))
                for file in files_to_download:
                    logging.info('Downloading %s' % file)
                    file_counter += 1
                    filename = posixpath.basename(urlparse.urlsplit(file).path)
                    output_path = os.path.join(args_.output_dir, filename)
                    if os.path.exists(output_path):
                        output_path += "-" + str(file_counter)
                    try:
                        urlretrieve(file, output_path)
                    except Exception:
                        logging.exception('Error downloading %s.', file)
            except Exception:
                logging.exception('Error fetching repository %s.', line)
    args_.yara_meta = os.path.join(args_.output_dir, args_.yara_meta)
    with open(args_.yara_meta, 'w') as f:
        for i in os.listdir(args_.output_dir):
            try:
                f.write("include \"" + i + "\"\n")
            except Exception:
                logging.exception('Couldn\'t write to %s.', args_.yara_meta)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Github file downloader")
    parser.add_argument("-r",
                        "--repo_file",
                        help="Path for the input file which contains a url of a Github repository "
                             "for each separate line")

    parser.add_argument("-w",
                        "--wildcard",
                        help="Unix shell-style wildcard to match files to download (for example: *.txt)")

    parser.add_argument("-o",
                        "--output_dir",
                        default="",
                        help="Directory to store all downloaded files")

    parser.add_argument("-y",
                        "--yara-meta",
                        default="rules.yara",
                        help="Yara meta rule filename to create")

    parser.add_argument("-t",
                        "--timeout",
                        default=30,
                        help="Socket timeout (seconds)")

    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    main(args, log_level)
