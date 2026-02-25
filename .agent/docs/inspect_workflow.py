import json
import os

file_path = r"D:\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LTX-Video_T2V_Full.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total nodes: {len(data['nodes'])}")
    
    for node in data['nodes']:
        title = node.get('title', node.get('type', 'Unknown'))
        node_type = node.get('type', 'Unknown')
        node_id = node.get('id')
        widgets = node.get('widgets_values', [])
        
        print(f"ID: {node_id} | Type: {node_type} | Title: {title}")
        print(f"  Widgets: {widgets}")
        print("-" * 40)

except Exception as e:
    print(f"Error: {e}")
