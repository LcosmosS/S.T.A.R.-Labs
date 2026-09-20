# docker/Dockerfile (fixed)
FROM mambaorg/micromamba:2.3.2-debian12

ARG USER=star
ARG UID=1000
ARG CONDA_ENV=star-env
ARG PYTHON_VERSION=3.12

ENV PATH=/opt/conda/bin:$PATH
SHELL ["/bin/bash", "-lc"]

# Run package installation as root
USER root

# Minimal system deps
RUN mkdir -p /var/lib/apt/lists/partial \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates wget curl git build-essential cmake pkg-config \
    libffi-dev libssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Create conda env and install binary TDA packages from conda-forge
RUN micromamba create -y -n ${CONDA_ENV} python=${PYTHON_VERSION} -c conda-forge \
    numpy scipy pandas plotly scikit-learn\
    gudhi=3.12.0 ripser=0.6.14 persim=0.3.8 \
    plotly=5.18.0 nbconvert nbclient jupyter_core ipykernel \
 && micromamba clean --all --yes

# Make the conda env the default for subsequent RUN steps
ENV CONDA_DEFAULT_ENV=${CONDA_ENV}
ENV CONDA_PREFIX=/opt/conda/envs/${CONDA_ENV}
ENV PATH=${CONDA_PREFIX}/bin:${PATH}

# Create non-root user only if missing (robust)
RUN if id -u ${USER} >/dev/null 2>&1; then \
      echo "user ${USER} already exists"; \
    else \
      if id -u ${UID} >/dev/null 2>&1; then \
        echo "UID ${UID} already taken, creating ${USER} without explicit UID"; \
        useradd -m ${USER}; \
      else \
        useradd -m -u ${UID} ${USER}; \
      fi; \
    fi

WORKDIR /home/${USER}/app
COPY . /home/${USER}/app
RUN chown -R ${USER}:${USER} /home/${USER}/app

# Install package into the conda env using the env's python (run as root)
# This guarantees the editable install uses the exact interpreter that has gudhi/ripser
RUN micromamba run -n ${CONDA_ENV} python -m pip install --upgrade pip setuptools wheel \
 && micromamba run -n ${CONDA_ENV} python -m pip install --no-cache-dir -e ".[dev,tda]"

# Switch to non-root user for runtime
USER ${USER}

# Ensure PYTHONPATH is defined and points to the app
ENV PYTHONPATH=/home/${USER}/app
WORKDIR /home/${USER}/app

# Default verification command (override in CI)
CMD ["bash", "-lc", "python -c \"import sys, gudhi, ripser; print('py', sys.version.split()[0], 'gudhi', gudhi.__version__, 'ripser', ripser.__version__)\""]
