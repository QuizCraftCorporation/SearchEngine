# Search Engine Server
Service for semantic search among any text. Used for quiz search.
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

## How to use
### Searching for text
Post request to http://**base_url**/search/
<br/>
Example of request body:
```JSON
{
	"query": "Psychology",
	"number_of_results": 3
}
```
Example of response body:
```JSON
{
"operation": "SUCCESS",
"payload": [
    {
      "raw_quiz_data": "...",
      "unique_id": "123"
    }
  ] 
}
```
### Saving text
Post request to http://**base_url**/search/
<br/>
Example of request body:
```JSON
{
	"raw_quiz_data": "...",
	"unique_id": "123"
}
```
Example of response body:
```JSON
{
	"operation": "SUCCESS"
}
```
