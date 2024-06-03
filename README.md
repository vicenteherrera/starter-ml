
# Requirements

* pyenv
* poetry

C:\Users\vicen\AppData\Roaming\Python\Scripts\poetry

Windows CUDA drivers:
* https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html
* https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local
* https://docs.nvidia.com/cuda/wsl-user-guide/index.html

## API Keys:

Open AI
* https://platform.openai.com/account/api-keys

Hugging Face
* 

## Examples

LMQL:
* https://lmql.ai/

## Troubleshooting:


### libcudnn.so

`libcudnn.so.8: cannot open shared object file: No such file or directory`  
* Make sure to install the latest `torch` library that works with CUDA driver on Windows native or WSL.
* You must not install any NVIDIA GPU Linux driver within WSL 2

### _ctypes

ModuleNotFoundError: No module named '_ctypes'  
* You have to install libffi-devel before installing the specific python version
  `sudo apt-get install libffi-dev`  
* Reinstall after that the PyEnv Python version in the project folder with:
```console
pyenv uninstall $(cat .python-version)
pyenv install $(cat .python-version)
```
