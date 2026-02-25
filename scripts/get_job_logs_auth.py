import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TOKEN = "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"

try:
    # Get latest run
    req = urllib.request.Request('https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/workflows/train_model_webhook.yml/runs')
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Authorization', f'Bearer {TOKEN}')
    
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if not data['workflow_runs']:
            print("No runs found")
            exit()
            
        run = data['workflow_runs'][0]
        
        # Get jobs
        jreq = urllib.request.Request(run['jobs_url'])
        jreq.add_header('User-Agent', 'Mozilla/5.0')
        jreq.add_header('Authorization', f'Bearer {TOKEN}')
        
        with urllib.request.urlopen(jreq, context=ctx) as jresp:
            jdata = json.loads(jresp.read().decode())
            for job in jdata['jobs']:
                if job['name'] == 'run-ai-model':
                    print(f"Fetching logs for job ID {job['id']}...")
                    log_url = f"https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/jobs/{job['id']}/logs"
                    try:
                        lreq = urllib.request.Request(log_url)
                        lreq.add_header('User-Agent', 'Mozilla/5.0')
                        lreq.add_header('Authorization', f'Bearer {TOKEN}')
                        with urllib.request.urlopen(lreq, context=ctx) as lresp:
                            logs = lresp.read().decode('utf-8')
                            lines = logs.split('\n')
                            print("--- LOG TIMESTAMP EXCERPT ---")
                            print('\n'.join(lines[-50:]))
                    except urllib.error.HTTPError as e:
                        print(f"HTTP Error fetching logs: {e.code} - {e.reason}")
                    break
except Exception as e:
    print(f"Error: {e}")
