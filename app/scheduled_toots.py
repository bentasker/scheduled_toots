#!/usr/bin/env python3
#
# Check for scheduled messages and send them if the time is right
#
#


import os
import sys
from datetime import datetime as dt


def triggerJobs(jobs, oldjob_dir, runtime):
    ''' Iterate through jobs checking time against now
    
    Trigger those which need triggering
    '''
    
    today = runtime.strftime("%Y-%m-%d")
    today_dir = f"{oldjob_dir}/{today}"
    
    for job in jobs:
        if not job["publish_at"]:
            # job was scheduled without a time, flag but ignore
            # TODO: should we have an "errored" dir in the heirachy?
            print(f"Err: Job {job['fname']} has no parseable time", file=sys.stderr)
            continue
        
        # Parse the date
        try:
                pub_date = dt.strptime(job["publish_at"], '%Y-%m-%dT%H:%M:%S%Z').astimezone()
        except Exception as e:
            print(f"Err: Job {job['fname']} time failed to parse {e}", file=sys.stderr)
            continue            

        # Check if the toot is due
        if pub_date <= runtime:
            # RUN!
            try:
                print("Send toot")
            except Exception as e:
                print(f"Err: Job {job['fname']} failed to run correctly {e}", file=sys.stderr)

            # Either way, move the file out of the way
            if not os.path.exists(today_dir):
                os.makedirs(today_dir)
            
            fname = os.path.basename(job["fname"])
            os.rename(job["fname"], f"{today_dir}/{fname}")
            



def loadJobs(newjob_dir):
    ''' Check for job files in the new dir and
    load them
    '''
    jobs = []
    for f in os.listdir(newjob_dir):
        if f.endswith(".swp"):
            # Some muppet left nano open
            continue
        jobs.append(loadJobFile(f"{newjob_dir}/{f}"))

    return jobs

        
def loadJobFile(file_path):
    ''' Load and parse a jobfile
    '''
    fh = open(file_path, 'r')
    f = {
        "publish_at" : False,
        "fname" : file_path
        }
    
    text_buffer = []
    have_date = False
    for line in fh.readlines():
        line_low = line.lower()
        
        # We're looking for a dateline
        if not have_date and line_low.startswith("date:"):
            l_sp = line.split(":")
            f["publish_at"] = ":".join(l_sp[1:]).strip()
            have_date = True
            continue
        
        if not have_date and line_low.startswith("time:"):
            # Provided with a time, parse that into a date
            l_sp = line.strip().split(":")
            t = ":".join(l_sp[1:]).strip()
            if len(l_sp) < 4:
                # Append seconds
                t += ":00"
            n = dt.now().astimezone()
            tz = n.strftime('%Z')
            f["publish_at"] = n.strftime('%Y-%m-%dT') +  t + tz
            have_date = True
            continue
        
        # Otherwise, buffer
        text_buffer.append(line)
        
    # The lines already have trailing newlines, so no need to include
    # in join
    f["text"] = "".join(text_buffer).lstrip("\n")
    
    if f["publish_at"].endswith("Z"):
        f["publish_at"] = f["publish_at"].replace("Z", "UTC")
    
    return f


if __name__ == "__main__":
    job_dir = os.getenv("JOB_DIR", "/jobs")
    runtime = dt.now().astimezone()
    # Check that the heirachy exists
    paths = {}
    for sub in ["new", "done"]:
        paths[sub] = f"{job_dir}/{sub}"
        if not os.path.exists(f"{job_dir}/{sub}"):
            os.makedirs(f"{job_dir}/{sub}")
            

    jobs = loadJobs(paths["new"])
    triggerJobs(jobs, paths["done"], runtime)

            
