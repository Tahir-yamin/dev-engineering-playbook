import urllib.request
import json

try:
    req = urllib.request.Request('https://api.github.com/repos/Tahir-yamin/dev-engineering-playbook/actions/runs')
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if 'workflow_runs' in data and len(data['workflow_runs']) > 0:
            for run in data['workflow_runs'][:3]:
                print(f"Name: {run.get('name')}")
                print(f"Status: {run.get('status')}")
                print(f"Conclusion: {run.get('conclusion')}")
                print(f"URL: {run.get('html_url')}")
                print("-" * 20)
        else:
            print('No workflow runs found.')
except Exception as e:
    print(f'Error: {e}')
