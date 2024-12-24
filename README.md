# WebsiteCollectAndAnalysis



## Configure

```shell
sudo apt-get install whois
```

```shell
pip install -r requirements.txt
```

## Run
First Run: collect_gwy.py and collect_provience.py, it may take hours to run it(it's a bug, i have no idea about it).
```shell
python3 collect_gwy.py
```
Open a new terminal and run
Notice: You should make sure your current work dir is in the project.

something like /***/WebsiteCollectAndAnalysis
```shell
python3 collect_provience.py
```
And then you can run unzip_gwy.py and unzip_sheng.py, since you run the above file which will download a lot of zip file.

```shell
python3 unzip_gwy.py
```

```shell
python3 unzip_sheng.py
```


After that, we will further process these file. I have download and unzip all of them.
```shell
python3 merger_csv.py
```
It will merger all file under the directory of /total_csv and output the result to /mergerd_csv


## Dependency

```shell
pip freeze > requirements.txt
```