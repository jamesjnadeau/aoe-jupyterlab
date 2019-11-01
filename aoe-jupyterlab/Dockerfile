FROM jupyter/scipy-notebook:1386e2046833

ENV JUPYTER_ENABLE_LAB yes

# Install the packages we need
RUN conda install --yes -c conda-forge "nodejs=10.8" ipywidgets ipython-sql pymssql pyodbc \
  python-dotenv nbstripout cx_Oracle papermill pywinauto r-irkernel chardet watchdog Faker && \
  conda clean -a
RUN pip install "jupyterlab==1.1.4" voila

# Lab Extensions
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.0 --no-build && \
  jupyter labextension install @jupyterlab/celltags --no-build && \ 
  jupyter labextension install @jupyterlab/toc --no-build
  # this is not working..? I can't seem to get it to fail when I run it manually inside the above layer.
  # build and clean assets, from: https://github.com/jupyterlab/jupyterlab/issues/4930#issuecomment-446597498
  # jupyter lab build && \
  # jupyter lab clean && \
  # jlpm cache clean && \
  # npm cache clean --force && \
  # rm -rf $HOME/.node-gyp && \
  # rm -rf $HOME/.local 

# Copy in our custom extension that loads our init.ipynb 
COPY --chown=$NB_UID:$NB_GID aoe_init.py /home/$NB_USER/.ipython/extensions/aoe_init.py

# fix permissions on folders so end user can do as they wish
RUN fix-permissions $CONDA_DIR && \
  fix-permissions /home/$NB_USER