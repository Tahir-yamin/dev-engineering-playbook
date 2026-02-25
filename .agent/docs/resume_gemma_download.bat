@echo off
cd /d "D:\my-dev-knowledge-base"
echo Resuming Gemma 13GB Download...
curl.exe -L -C - -o "D:\my-dev-knowledge-base\ComfyUI_Bridge\ComfyUI_windows_portable\ComfyUI\models\text_encoders\gemma-3-12b-it-fp8\gemma_3_12B_it_fp8_scaled.safetensors" "https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors?download=true"
pause
