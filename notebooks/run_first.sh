CMAKE_ARGS="-DGGML_CUDA=on" 
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir --no-binary llama-cpp-python
pip install huggingface-hub
pip install hf_transfer
