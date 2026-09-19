# Cryptographic law scaffolds

[sha256-obligations.json](sha256-obligations.json) enumerates joint participants and premises for the first hash implementation. It is an implementation inventory. The compiler does not consume this file and it contains no admitted theorem or proof certificate.

The intended law packages use typed proof quotations or checked Rocq theorem bindings under the [Clef proof plan](../docs/clef-proof-plan.md). Their applications become joint constraints in the PHG. Each application must retain the actual operand identities, arithmetic construction and governing premises.

For the first modular-addition law, the mathematical contract is:

```text
q = 2^32
0 <= a < q, 0 <= b < q
s = a + b                  exact intermediate, capacity through 2q - 2
r = s % q
--------------------------------------------
0 <= r < q, and r is congruent to a + b modulo q
```

The explicit reduction in the source gives SHA-256 its required modular semantics. DTS range analysis determines the intermediate carrier. A target instruction that wraps at 32 bits needs a checked equivalence to that whole source operation before it can replace the exact sum followed by reduction.

A quotation can state this proposition, but admission requires its derivation. The compression law must then relate the actual state and schedule to the reference function. Its premises cannot be replaced with a successful vector test or a proof about a different representation.
