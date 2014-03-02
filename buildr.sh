#!/usr/bin/env bash

_TMP_PWD=$PWD
BASEDIR=$(dirname $0)

banner(){
  echo "///////////////////////////////////////////"
  echo -e $@
  echo "///////////////////////////////////////////"
}

prepare_virtualenv(){
  _VENV_DIR=$1
  if [ ! -d $1 ]; then
    _VENV_DIR=$PWD
  fi
  banner "Preapring Virtualenv for "$(basename $_VENV_DIR)
  if [ ! -f $_VENV_DIR/.venv/bin/activate ]; then
    virtualenv2 "${_VENV_DIR}/.venv"
  fi
  source $_VENV_DIR/.venv/bin/activate
  pip install -r $_VENV_DIR/requirements.txt
}

build_init_nova_agent(){
  if [ -d ./dist/nix-bootstrapper ]; then
    banner "Cleaning earlier $PWD/dist/nix-bootstrapper"
    rm -rf ./dist/nix-bootstrapper
  fi

  prepare_virtualenv $BASEDIR

  banner "Running PyInstaller"
  $BASEDIR/.venv/bin/pyinstaller nix-bootstrapper.spec

  banner "Building Distributable"
  cd ./dist
  tar czvf nix-bootstrapper.tgz nix-bootstrapper
  echo "distributable generated at: $BASEDIR/dist/nix-bootstrapper.tgz"
}


cd $BASEDIR

if [ "$1" == "build" ]; then
  build_init_nova_agent

elif [ "$1" == "clean" ]; then
  banner "Cleaning up build created data..."
  rm -rf *.pyc **/*.pyc
  rm -rf $BASEDIR/dist
  rm -rf $BASEDIR/build

elif [ "$1" == "venv" ]; then
  banner "Preparing Virtualenv"
  prepare_virtualenv $BASEDIR

else
  banner "[build your package]\n\tSyntax: $0 build"
  exit 1

fi

cd $_TMP_PWD

banner "nix-bootstrapper Buildr is finished working..."
