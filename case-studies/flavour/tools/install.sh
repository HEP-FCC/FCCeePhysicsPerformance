if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ${0} <LOCALPATH>"
    echo "Where <LOCALPATH> is the local path where to install the extra packages"
    echo "Example local path: localPythonTools"
    return 1
fi

mkdir -p ${1}
export PYTHONUSERBASE=${1}/.local

echo "> getting latest pip"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

rm get-pip.py

export PATH=${1}/.local/bin:$PATH


python -m pip install --user zfit
python -m pip install --user xgboost
python -m pip install --user pandas
python -m pip install --user root_pandas
python -m pip install --user sklearn
python -m pip install --user scipy

export PYTHONPATH=${1}/.local/lib/python3.7/site-packages:$PYTHONPATH


