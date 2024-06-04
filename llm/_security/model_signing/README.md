# model_signing

Sign models and verify model signature.

Based on https://github.com/sigstore/model-transparency/blob/main/model_signing/README.md

```console
# Requirements
sudo apt install git git-lfs
git lfs install

# Sparese clone the mode_signing directory in the model-transparecy repo
git clone -n --depth=1 --filter=tree:0 git@github.com:sigstore/model-transparency.git
cd model-transparency
git sparse-checkout set --no-cone model_signing
git checkout
```