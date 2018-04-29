import urllib
import json
import sys
import time, os
from bs4 import BeautifulSoup

MAX_SUBS = 1000000
MAX_CF_CONTEST_ID = 600
MAGIC_START_POINT = 17000

if (len(sys.argv) < 2):
    print 'Usage: python main.py <handle>'
    exit(1)

handle = sys.argv[1]

DOWNLOAD_DIR = 'Solutions'
SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'
USER_INFO_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
keys = replacer.keys()

def get_ext(comp_lang):
    if 'C++' in comp_lang:
        return 'cpp'
    for key in EXT_keys:
        if key in comp_lang:
            return EXT[key]
    return ""

def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])
    return source_code

base_dir = DOWNLOAD_DIR + '/' + handle
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

user_info = urllib.urlopen(USER_INFO_URL.format(handle=handle, count=MAX_SUBS)).read()
dic = json.loads(user_info)
if dic['status'] != u'OK':
    print 'Oops.. Something went wrong...'
    exit(0)

submissions = dic['result']
start_time = time.time()

for submission in submissions:
    if submission['verdict'] == u'OK' and submission['contestId'] < MAX_CF_CONTEST_ID:
        con_id, sub_id = submission['contestId'], submission['id'],
        prob_name, prob_id = submission['problem']['name'], submission['problem']['index']
        comp_lang = submission['programmingLanguage']
        submission_full_url = SUBMISSION_URL.format(ContestId=con_id, SubmissionId=sub_id)
        print 'Fetching %s' % submission_full_url
        submission_info = urllib.urlopen(submission_full_url).read()
        soup = BeautifulSoup(submission_info, 'html.parser')
        submission_text = soup.find('pre', id='program-source-text')
        result = submission_text.text.replace('\r', '')
        ext = get_ext(comp_lang)
        new_directory = base_dir + '/' + str(con_id)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        file = open(new_directory + '/' + prob_id + '[ ' + prob_name + ' ]' + '.' + ext, 'w')
	file.write(result)
	file.close()		
end_time = time.time()

print 'Finished in %d seconds' % int(end_time - start_time)
