# Aspa f-spexet
Generates asp-posters for f-spexet

## Usage
To run `script.py`, you first need to install python3 (and pip3).

1. Install reportlab (and imghdr if you are using the newest version of python)
```
pip3 install reportlab
pip3 install standard-imghdr
```

2. Download this repo
```
git clone https://github.com/TheCoder5550/aspa-f-spexet.git
cd aspa-f-spexet
```

3. Upload images and texts:
* Place images inside `input/bilder`
* Comma-seperated text in `input/texter.csv`
* Additional sub text in `input/subtext.txt`
* Bottom text in `input/bottomtext.txt`
* Change `input/loggan.png` to your logo

4. Run the script
```
python3 script.py
```

I have tried the script with png's and jpg's as image formats. Maybe others work, maybe not.