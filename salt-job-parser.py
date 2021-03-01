#!/usr/bin/env python3

# Salt Job Parser
# Copyright (C) 2021 James Harris, Immersive Labs
# https://github.com/Immersive-Labs-Sec/SaltStackTools

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import msgpack
import json
import argparse
from pprint import pprint

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "-dir", "--directory", nargs='?', help="Path to the jobs directory.")

    args = parser.parse_args()

    if args.directory:

        jobs_dir = str(args.directory)
        if '~' in jobs_dir:
            jobs_dir = os.path.expanduser(jobs_dir)

        if not os.path.exists(jobs_dir):
            print("[ERROR] '" + jobs_dir + "' is not a valid directory.")
            exit(-1)

        for subdir, dirs, files in os.walk(jobs_dir):

            for file in files:

                if file == 'jid':
                    full_path = subdir + "/" + file
                    with open(full_path, 'r') as f:
                        jid = f.read()
                    print('Job ID: ' + jid)
                    f.close()

                if file == '.minions.p':
                    print("MINIONS File:")
                    full_path = subdir + "/" + file
                    with open(full_path, 'rb') as f:
                        file_content = f.read()
                        decoded_response = msgpack.unpackb(file_content)
                        print(decoded_response)
                        f.close()

                if file == '.load.p':
                    print("LOAD File:")
                    full_path = subdir + "/" + file
                    with open(full_path, 'rb') as f:
                        file_content = f.read()
                        decoded_response = msgpack.unpackb(file_content)
                        json_format = (json.dumps(decoded_response, indent=4, sort_keys=True))
                        print(json_format)
                        f.close()

                if file == 'return.p':
                    print("RETURN File:")
                    full_path = subdir + "/" + file

                    with open(full_path, 'rb') as f:
                        file_content = f.read()
                        decoded_response = msgpack.unpackb(file_content)
                        pprint(decoded_response)
                        f.close()
                        # blank line to help separate each job.
                        print()

    else:
        print("[ERROR] Please specify the path to the jobs directory.")
        exit(-1)
