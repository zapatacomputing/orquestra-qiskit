############################################################################
#   Copyright 2017 Rigetti Computing, Inc.
#   Modified by Zapata Computing 2020 to work for qiskit's SummedOp.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
############################################################################

import numpy as np
import pytest
from orquestra.quantum.openfermion.ops import (
    FermionOperator,
    InteractionOperator,
    InteractionRDM,
)
from orquestra.quantum.wip.operators import PauliSum, PauliTerm
from qiskit.opflow import PauliOp, SummedOp
from qiskit.quantum_info import Pauli

from orquestra.integrations.qiskit.conversions import (
    qiskitpauli_to_qubitop,
    qubitop_to_qiskitpauli,
)


def test_translation_type_enforcement():
    """
    Make sure type check works
    """
    create_one = FermionOperator("1^")
    empty_one_body = np.zeros((2, 2))
    empty_two_body = np.zeros((2, 2, 2, 2))
    interact_one = InteractionOperator(1, empty_one_body, empty_two_body)
    interact_rdm = InteractionRDM(empty_one_body, empty_two_body)

    with pytest.raises(TypeError):
        qubitop_to_qiskitpauli(create_one)
    with pytest.raises(TypeError):
        qubitop_to_qiskitpauli(interact_one)
    with pytest.raises(TypeError):
        qubitop_to_qiskitpauli(interact_rdm)


def test_paulisum_to_qiskitpauli():
    """
    Conversion of PauliSum to qiskit SummedOp; accuracy test
    """
    pauli_term = PauliSum.from_str("0.5*X0*Z1*X2 + 0.5*Y0*Z1*Y2")

    qiskit_op = qubitop_to_qiskitpauli(pauli_term)

    ground_truth = (
        PauliOp(Pauli.from_label("XZX"), 0.5) + PauliOp(Pauli.from_label("YZY"), 0.5)
    ).to_pauli_op()

    assert ground_truth == qiskit_op


def test_pauliterm_to_qiskitpauli():
    """
    Conversion of PauliTerm to qiskit SummedOp; accuracy test
    """
    pauli_term = PauliTerm.from_str("2.25*Y0*X1*Z2*X4")

    qiskit_op = qubitop_to_qiskitpauli(pauli_term)

    ground_truth = SummedOp([PauliOp(Pauli.from_label("YXZIX"), 2.25)])

    assert ground_truth == qiskit_op


def test_qubitop_to_qiskitpauli_zero():
    zero_term = PauliSum()
    qiskit_term = qubitop_to_qiskitpauli(zero_term)
    ground_truth = SummedOp([])

    assert ground_truth == qiskit_term


def test_qiskitpauli_to_qubitop():
    """
    Conversion of qiskit SummedOp to PauliSum; accuracy test
    """
    qiskit_term = SummedOp([PauliOp(Pauli.from_label("XIIIIY"), coeff=1)])

    expected_pauli_term = PauliTerm.from_list([("X", 0), ("Y", 5)])
    test_pauli_term = qiskitpauli_to_qubitop(qiskit_term)

    assert test_pauli_term == expected_pauli_term


def test_qiskitpauli_to_qubitop_type_enforced():
    """Enforce the appropriate type"""
    create_one = FermionOperator("1^")
    empty_one_body = np.zeros((2, 2))
    empty_two_body = np.zeros((2, 2, 2, 2))
    interact_one = InteractionOperator(1, empty_one_body, empty_two_body)
    interact_rdm = InteractionRDM(empty_one_body, empty_two_body)

    with pytest.raises(TypeError):
        qiskitpauli_to_qubitop(create_one)
    with pytest.raises(TypeError):
        qiskitpauli_to_qubitop(interact_one)
    with pytest.raises(TypeError):
        qiskitpauli_to_qubitop(interact_rdm)
