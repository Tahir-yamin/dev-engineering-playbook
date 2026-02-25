import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request('https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/runs/22036823476/jobs')
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if 'jobs' in data:
            for job in data['jobs']:
                if job['name'] == 'run-ai-model':
                    print(f"Log URL: {job['html_url']}")
                    break
except Exception as e:
    print(f"Error: {e}")
