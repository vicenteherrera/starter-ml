
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

`libcudnn.so.8: cannot open shared object file: No such file or directory`
* Make sure to install the `torch` library that works with CUDA driver on Windows native or WSL.
* You must not install any NVIDIA GPU Linux driver within WSL 2
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

https://joelognn.medium.com/installing-wsl2-pytorch-and-cuda-on-windows-11-65a739158d76

https://pytorch.org/get-started/locally/


poetry source add --priority=supplemental torch-cuda11.8 https://download.pytorch.org/whl/cu118

poetry add --source torch-cuda11.8 torch --platform wsl


torch = [
  {version = "^2.1.0", platform = "darwin"},
  {version = "^2.1.0+cu118", platform = "windows", source = "torch-cuda11.8"},
  {version = "^2.1.0+cu118", platform = "linux", source = "torch-cuda11.8"}
  ]
