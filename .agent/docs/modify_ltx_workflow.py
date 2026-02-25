import json

input_path = r"D:\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LTX-Video_T2V_Full.json"
output_path = r"D:\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LTX-Video_T2V_Ready.json"

models = {
    "checkpoint": r"LTX-Video\ltx-2-19b-dev-fp8.safetensors",
    "gemma": "gemma_3_12B_it_fp8_scaled.safetensors",
    "sampler": "euler"
}

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for node in data['nodes']:
    node_type = node.get('type')
    
    if node_type == 'CheckpointLoaderSimple':
        # Widget 0 is usually ckpt_name
        if len(node['widgets_values']) > 0:
            node['widgets_values'][0] = models['checkpoint']
            print(f"Updated Checkpoint to {models['checkpoint']}")

    elif node_type == 'LTXVGemmaCLIPModelLoader':
        # Identify widgets by looking at current values or index (usually 0=gemma, 1=ltx model matching)
        # Based on user error: gemma_path is usually first.
        if len(node['widgets_values']) > 0:
             node['widgets_values'][0] = models['gemma']
             # Often second widget is the LTX model filename for some validation/pairing
             if len(node['widgets_values']) > 1:
                 node['widgets_values'][1] = models['checkpoint'] 
             print(f"Updated GemmaLoader to {models['gemma']}")

    elif node_type == 'KSamplerSelect':
        if len(node['widgets_values']) > 0:
            node['widgets_values'][0] = models['sampler']
            print(f"Updated Sampler to {models['sampler']}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Saved modified workflow to {output_path}")
