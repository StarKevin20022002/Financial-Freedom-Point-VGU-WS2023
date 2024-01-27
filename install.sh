conda activate base
conda create -n p3_env python=3.7 -y
conda activate p3_env
conda install -c conda-forge streamlit -y
conda install -c anaconda pandas -y
conda install -c anaconda numpy -y
pip install plotnine
pip install Pillow