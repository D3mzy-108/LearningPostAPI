<!--
The following commands are required for downloading the spaCy model and BERT model components.
These commands download language models for spaCy and pretrained weights for the BERT model.
-->

pip install torch
pip install tensorflow

<!-- IF IN AKADA'S VIEWS.PY, nlp = spacy.load("en_core_web_sm") -->

python -m spacy download en_core_web_sm

<!-- ELSE IF nlp = spacy.load("en_core_web_md") -->

python -m spacy download en_core_web_md

<!-- ELSE IF nlp = spacy.load("en_core_web_lg") -->

python -m spacy download en_core_web_lg

<!-- INSTALL NECESSARY TRANSFORMERS MODELS -->

python -m transformers.models.bert.tokenization_bert download_pretrained
python -m transformers.models.bert.modeling_bert download_pretrained

<!--
Make sure to run these commands while your virtual environment is active.

These steps ensure that the required libraries and language models are installed and available for your
Django project.
-->
