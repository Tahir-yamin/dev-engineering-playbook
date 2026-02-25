import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request('https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/workflows/train_model_webhook.yml/runs')
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if 'workflow_runs' in data and len(data['workflow_runs']) > 0:
            run = data['workflow_runs'][0]
            print(f"Run name: {run['name']}, Status: {run['status']}, Conclusion: {run['conclusion']}")
            
            # get jobs
            jobs_url = run['jobs_url']
            jreq = urllib.request.Request(jobs_url)
            jreq.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(jreq, context=ctx) as jresp:
                jdata = json.loads(jresp.read().decode())
                for job in jdata['jobs']:
                    print(f"  Job: {job['name']} - {job['conclusion']}")
                    if job['conclusion'] == 'failure':
                        for step in job['steps']:
                            if step['conclusion'] == 'failure':
                                print(f"    Failed Step: {step['name']}")
        else:
            print('No runs found for this workflow.')
except Exception as e:
    print(f"Error: {e}")
