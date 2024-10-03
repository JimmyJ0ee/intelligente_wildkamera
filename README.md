# Intelligente Wildkamera

### Installation

1. ``Create Environment from requirement.txt and activate like shown below.``
2. ``Connect to the zf-iasdnternal net e.g. via VPN.``
3. ``Open PTC-Windchill and log in.``
4. ``Execute main.py. Make sure your terminal is in "./PATs/src/"``

### Environment Commands

###### Create env

```
python -m venv <env-name> 
```

###### Activate env

```
".venv/Scripts/activate" 

bei Fehler bis in Scripts navigieren und dann nur "acitvate eingeben"
```

###### Deactivate env

```
deactivate
```

###### List of all installed packages

```
pip list
```

###### Export env

```
pip freeze > requirements.txt
```

###### Import env

```
pip install -r requirements.txt
```