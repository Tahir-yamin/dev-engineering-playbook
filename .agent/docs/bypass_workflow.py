import json
import os

input_path = r"D:\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LTX-Video_T2V_Ready.json"
output_path = r"D:\Downloads\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LTX-Video_Possible_Run.json"

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

nodes = data['nodes']
links = data['links']

# Helper to find node by type
def find_node_by_type(node_type):
    for node in nodes:
        if node['type'] == node_type:
            return node
    return None

# Helper to find link by target node/slot
def find_link_to_node_input(node_id, slot_index):
    for link in links:
        # Link format: [id, origin_id, origin_slot, target_id, target_slot, type]
        if link[3] == node_id and link[4] == slot_index:
            return link
    return None

# Helper to find links originating from a node
def find_links_from_node(node_id):
    found = []
    for link in links:
        if link[1] == node_id:
            found.append(link)
    return found

# 1. Bypass LoRA
# Strategy: Find what feeds INTO LoRA (Model), find what LoRA feeds OUT to, connect them directly.
lora_node = find_node_by_type('LoraLoaderModelOnly')
if lora_node:
    print("Found LoRA node to bypass.")
    lora_id = lora_node['id']
    
    # Input is usually slot 0 (MODEL) or 1 (CLIP) - for ModelOnly it's 0
    input_link = find_link_to_node_input(lora_id, 0) # Link coming IN
    
    if input_link:
        source_node_id = input_link[1]
        source_slot_id = input_link[2]
        
        # Find all outputs from LoRA
        output_links = find_links_from_node(lora_id)
        
        for out_link in output_links:
            # Redirect to source
            out_link[1] = source_node_id
            out_link[2] = source_slot_id
            print(f"Redirected link {out_link[0]} to confirm bypass.")
        
        # Remove the node and the input link
        nodes.remove(lora_node)
        links.remove(input_link)
        print("Removed LoRA node.")

# 2. Bypass Upscaler
# Strategy: Latent Upscaler usually takes LATENT in, outputs LATENT.
upscale_node = find_node_by_type('LatentUpscaleModelLoader')
# Wait, Upscale MODEL loader doesn't take latent, it outputs a MODEL to a "LatentUpscale" node.
# If we remove the loader, the Upscale node will fail. 
# We need to find the actual "LatentUpscale" or "Upscale" node and bypass THAT.
# Let's see if we can just remove the Loader and the Upscale node itself?
# Or just reconnect Latent -> Sampler (or VAE Decode).

# Let's inspect connections for Upscaler Model Loader first.
# It likely feeds into "LatentUpscale" (ID 5262 from previous log looked like text, wait).
# Log showed "LatentUpscaleModelLoader" ID 14030? No that was link.
# Let's just remove the Upscaler Model Loader node and any node that DEPENDS on it? 
# Too risky. 
# Simpler: If the user says "Bypass", they usually bypass the *Process*.
# Let's try to just remove the specific "LatentUpscaleModelLoader" and see if we can find the "Upscale" node it feeds.

upscale_loader = find_node_by_type('LatentUpscaleModelLoader')
if upscale_loader:
    print("Found Upscale Loader.")
    loader_id = upscale_loader['id']
    
    # Find what it feeds
    out_links = find_links_from_node(loader_id)
    for link in out_links:
        target_node_id = link[3]
        print(f"Upscaler feeds node {target_node_id}")
        
        # This target node (likely 'LatentUpscale') needs to be bypassed too.
        # Find what feeds INTO this target node (The Latent image)
        # Usually slot 0 is samples/latent.
        latent_input_link = find_link_to_node_input(target_node_id, 0)
        
        if latent_input_link:
            latent_source_id = latent_input_link[1]
            latent_source_slot = latent_input_link[2]
            
            # Find what this target node outputs TO
            target_out_links = find_links_from_node(target_node_id)
            
            for t_link in target_out_links:
                # Redirect to the original latent source
                t_link[1] = latent_source_id
                t_link[2] = latent_source_slot
                print(f"Redirected upscale output link {t_link[0]} to source latent.")
            
            # Remove the Upscale node
            # We need to find the node object
            for n in nodes:
                if n['id'] == target_node_id:
                    nodes.remove(n)
                    print("Removed Upscale processing node.")
                    break
        
    nodes.remove(upscale_loader)
    print("Removed Upscale Loader node.")

# Save
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Saved bypassed workflow to {output_path}")
