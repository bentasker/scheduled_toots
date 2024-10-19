#!/usr/bin/env python3
#
# Check for scheduled messages and send them if the time is right
#
#


import os
from datetime import datetime as dt


def loadJobs(newjob_dir):
    ''' Check for job files in the new dir and
    load them
    '''
    jobs = []
    for f in os.listdir(newjob_dir):
        jobs.append(loadJobFile(f"{newjob_dir}/{f}"))

    return jobs

        
def loadJobFile(file_path):
    ''' Load and parse a jobfile
    '''
    fh = open(file_path, 'r')
    f = {
        "publish_at" : False
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
    
    return f


if __name__ == "__main__":
    job_dir = os.getenv("JOB_DIR", "/jobs")
    # Check that the heirachy exists
    paths = {}
    for sub in ["new", "done"]:
        paths[sub] = f"{job_dir}/{sub}"
        if not os.path.exists(f"{job_dir}/{sub}"):
            os.makedirs(f"{job_dir}/{sub}")
            

    jobs = loadJobs(paths["new"])
    

            
