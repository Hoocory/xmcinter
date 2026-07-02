# sets up xmc inter into your python environment
# to run...
# source setup_xmcinter.sh

XMCINTER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
XMCINTER_PARENT="$(dirname "$XMCINTER_DIR")"

export XMCINTER_DIR
export PYTHONPATH="$XMCINTER_PARENT:$PYTHONPATH"

echo "XMCINTER_DIR=$XMCINTER_DIR"
echo "Added $XMCINTER_PARENT to PYTHONPATH"
echo "Test with:"
echo "  python -c 'import xmcinter.xmcfiles as xf; print(xf)'"