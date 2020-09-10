import qiskit.providers.aer.noise as AerNoise
import qiskit.quantum_info.operators.channel as Channel
from typing import TextIO
import json
from zquantum.core.utils import SCHEMA_VERSION
from typing import Dict


def save_qiskit_noise_model(noise_model: AerNoise.NoiseModel, filename: str) -> None:
    """Save a qiskit aer noise model to file
    Args:
        noise_model (qiskit.providers.aer.noise.NoiseModel): the noise model to be saved
        filename (str): the name of the file
    """

    data = {
        "module_name": "qeqiskit.utils",
        "function_name": "load_qiskit_noise_model",
        "schema": SCHEMA_VERSION + "-noise-model",
        "data": noise_model.to_dict(serializable=True),
    }

    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=2))


def load_qiskit_noise_model(data: dict) -> AerNoise.NoiseModel:
    """Load a qiskit aer noise model object from file
    Args:
        data (dict): the serialized version of the qiskit noise model
    
    Returns:
        (qiskit.providers.aer.noise.NoiseModel): the noise model
    """
    return AerNoise.NoiseModel.from_dict(data)


def save_kraus_operators(kraus: Dict, filename: str ) -> None:
    """Save a kraus operator to file
    Args:
        kraus (Dict): Has single qubit and two qubit kraus operators
        filename (str): the name of the file
    
    """
    dict['schema'] = SCHEMA_VERSION+'-dict'

    with open(filename, 'w') as f:
        f.write(json.dumps(dict, indent=2))

def load_kraus_operators(file):
    """Load kraus dictionary from a file.
    Args:
        file (str or file-like object): the name of the file, or a file-like object.
    Returns:
        dict: the kraus dict.
    """

    if isinstance(file, str):
        with open(file, 'r') as f:
            data = json.load(f)
    else:
        data = json.load(file)

    return data


