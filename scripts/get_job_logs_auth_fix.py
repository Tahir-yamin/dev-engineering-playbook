import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TOKEN = "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"

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

try:
    req = urllib.request.Request('https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/workflows/train_model_webhook.yml/runs')
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Authorization', f'Bearer {TOKEN}')
    
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if not data['workflow_runs']:
            print("No runs found")
            exit()
            
        run = data['workflow_runs'][0]
        
        jreq = urllib.request.Request(run['jobs_url'])
        jreq.add_header('User-Agent', 'Mozilla/5.0')
        jreq.add_header('Authorization', f'Bearer {TOKEN}')
        
        with urllib.request.urlopen(jreq, context=ctx) as jresp:
            jdata = json.loads(jresp.read().decode())
            for job in jdata['jobs']:
                if job['name'] == 'run-ai-model':
                    print(f"Fetching logs for job ID {job['id']}...")
                    log_url = f"https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/jobs/{job['id']}/logs"
                    
                    opener = urllib.request.build_opener(NoRedirectHandler)
                    lreq = urllib.request.Request(log_url)
                    lreq.add_header('User-Agent', 'Mozilla/5.0')
                    lreq.add_header('Authorization', f'Bearer {TOKEN}')
                    try:
                        opener.open(lreq, timeout=10)
                    except urllib.error.HTTPError as e:
                        if e.code in (301, 302, 303, 307, 308):
                            redirect_url = e.headers.get('Location')
                            print(f"Redirected to: {redirect_url[:50]}...")
                            # Fetch without auth header
                            final_req = urllib.request.Request(redirect_url)
                            final_req.add_header('User-Agent', 'Mozilla/5.0')
                            with urllib.request.urlopen(final_req, context=ctx) as fresp:
                                logs = fresp.read().decode('utf-8')
                                lines = logs.split('\n')
                                print("--- LOG TIMESTAMP EXCERPT ---")
                                print('\n'.join(lines[-40:]))
                        else:
                            print(f"HTTP Error: {e.code}")
                    break
except Exception as e:
    print(f"Error: {e}")
