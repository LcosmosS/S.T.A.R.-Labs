mkdir -p /home/Kepler/star_docgen/{corpus,output}
cd /home/Kepler/star_docgen
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
