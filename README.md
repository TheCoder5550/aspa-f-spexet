To run `script.py`, you first need to install python3 (and pip3).

1. Install reportlab

```
pip3 install reportlab
```

2. Download this repo

```
git clone https://github.com/JohnTheDaniel/ASPA-pdf-gen.git
cd ASPA-pdf-gen
```

3. Run the script

```
python3 script.py
```

It will read pictures from "bilder" and the texts from the file "texter.csv", which need to formatted as comma seperated values.
The script needs a logo to place in the bottom right corner. It needs to have the name "loggan.xxx"

I have tried the script with png's and jpg's as image formats. Maybe others work, maybe not.

Be aware! Mac OSX likes to add a hidden file named `.DS_Store` in folders. Before running the script, you need to delete this file in from `bilder`.
To check if DS_Store is in your folder, write:
```
cd bilder
ls -la 
```

To remove it, type
```
rm .DS_Store
```
