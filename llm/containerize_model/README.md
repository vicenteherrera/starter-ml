# containerize_model

Containerize the code that employs model files for inference.

There are targets that explore including model files and not doing so in the container, as well as compiling the source Python code. 

This is a complex example that is not fully documented, you have to navigate the makefile to understand all cases covered. 

You can also check the [simple_local_mode](./simple_local_mode) directory for a simpler example.

The model will be downloaded from Huggingface. Set up a Huggingface account and set up your API token to avoid being throttled when downloading.

Check the generic instructions for requirements at parent [README.md](../../README.md).