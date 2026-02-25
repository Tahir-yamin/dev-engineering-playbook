# first line: 300
@memory.cache
def get_digits() -> Tuple[np.ndarray, np.ndarray]:
    """Fetch the digits dataset from sklearn."""
    datasets = pytest.importorskip("sklearn.datasets")
    data = datasets.load_digits()
    return data.data, data.target
