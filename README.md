# Search Engine Server
## How to install and run
1. Make sure that you have installed lfs
```console
git lfs install
```

2. Clone repository with submodules
```console
git clone --recurse-submodules https://github.com/QuizCraftCorporation/SearchEngine.git
```

3. Create virtual environment and install dependencies
```console
python -m venv venv
```
(activate for Windows)
```console
venv\Scripts\activate
```

```console
pip install -r requirements.txt
```

4. Run server with specified port and host address.
```console
py server.py --address 127.0.0.1 --port 1234
```
(you can set your own port and address if you want)