FROM jupyter/scipy-notebook:1386e2046833

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

USER $NB_UID

ENV JUPYTER_ENABLE_LAB yes

# Install the packages we need
RUN conda install --yes -c conda-forge "nodejs=10.8" ipywidgets ipython-sql pymssql pyodbc \
  python-dotenv nbstripout cx_Oracle papermill pywinauto r-irkernel chardet watchdog Faker \
  jupyterlab=1.2.1 voila jupyterlab-git\
  && conda clean -a

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
  
RUN jupyter serverextension enable --py jupyterlab_git

# Copy in our custom extension that loads our init.ipynb 
COPY --chown=$NB_UID:$NB_GID aoe_init.py /home/$NB_USER/.ipython/extensions/aoe_init.py
RUN jupyter notebook --generate-config -y

# fix permissions on folders so end user can do as they wish
RUN fix-permissions $CONDA_DIR && \
  fix-permissions /home/$NB_USER
