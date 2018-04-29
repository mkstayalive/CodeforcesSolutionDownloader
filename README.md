CodeforcesSolutionDownloader
============================

A small script for downloading *ACCEPTED* solutions from codeforces.com

Install the dependency `bs4`
```
pip install bs4
```

Run main.py and pass the user handle as argument

```
python main.py <user_handle>
```

For example,
```
python main.py Petr
```

It will create folders with the user handle and Codeforces rounds under `Solutions` folder and place the solutions there.
