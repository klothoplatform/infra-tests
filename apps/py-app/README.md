# Running

First, install the requirements. I suggset doing this within a virtualenv.

    pip install -r requirements.txt

Then:

    uvicorn app.main:app --port=3000 --reload

This will auto-reload whenever you make a change to the source. (You can disable that by removing `--reload`.)
