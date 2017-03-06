#!/usr/bin/env python
#

import sys, os, argparse, logging, fnmatch, posixpath, socket
import github

if sys.version_info < (3, 0):
    # python 2
    import urlparse
    from urllib import urlretrieve
else:
    # python 3
    import urllib.parse as urlparse
    from urllib.request import urlretrieve

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    socket.setdefaulttimeout(args.timeout)

    g = github.Github()

    if args.repo_file:
        with open(args.repo_file, 'r') as f:
            repo_gen = f
            download_files(args, g, repo_gen)
    else:
        def repo_gen():
            last_page = args.crawl_since
            git_repo_gen = g.get_repos(since=args.crawl_since)
            for repo in git_repo_gen:
                current_page = git_repo_gen.__nextUrl
                if current_page != last_page:
                    print("Finished processing: {}".format(current_page))
                    last_page = current_page
                yield repo
        download_files(args, g, repo_gen())

def download_files(args, g, repo_gen):
    file_counter = 0
    for line in repo_gen:
        logging.info('Fetching repository: %s' % line)
        try:
            repo_str = line.rstrip().split('github.com/')[-1]
            repo = g.get_repo(repo_str)
            tree = repo.get_git_tree('master', recursive=True)
            files_to_download = []
            for file in tree.tree:
                if fnmatch.fnmatch(file.path, args.wildcard):
                    files_to_download.append('https://github.com/%s/raw/master/%s' % (repo_str, file.path))
            for file in files_to_download:
                logging.info('Downloading %s' % file)
                file_counter += 1
                filename = posixpath.basename(urlparse.urlsplit(file).path)
                output_path = os.path.join(args.output_dir, filename)
                if os.path.exists(output_path):
                    output_path += "-" + str(file_counter)
                try:
                    urlretrieve(file, output_path)
                except Exception as e:
                    logging.exception('Error downloading %s.' % file)
        except Exception as e:
             logging.exception('Error fetching repository %s.' % line)

    args.yara_meta = os.path.join(args.output_dir, args.yara_meta)
    with open(args.yara_meta, 'w') as f:
        for i in os.listdir(args.output_dir):
            try:
                f.write("include \"" + i + "\"\n")
            except Exception as e:
                logging.exception('Couldn\'t write to %s.' % args.yara_meta)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Github file downloader")
    parser.add_argument("-r",
                        "--repo_file",
                        help = "Path for the input file which contains a url of a Github repository for each separate line")

    parser.add_argument("-p",
                        "--crawl_since",
                        default = github.GithubObject.NotSet,
                        help = "When not using a repo_file, this will be used as starting position for github repo crawl")

    parser.add_argument("-w",
                        "--wildcard",
                        help = "Unix shell-style wildcard to match files to download (for example: *.txt)")

    parser.add_argument("-o",
                        "--output_dir",
                        default = "",
                        help = "Directory to store all downloaded files")

    parser.add_argument("-y",
                        "--yara-meta",
                        default = "rules.yara",
                        help = "Yara meta rule filename to create")

    parser.add_argument("-t",
                        "--timeout",
                        default = 30,
                        help = "Socket timeout (seconds)")

    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
