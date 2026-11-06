# Vendored subset of openai/math

These files are an **unmodified copy** of part of [openai/math](https://github.com/openai/math)
at commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a)
(the full repository is about 1 GB, so only the files this explainer quotes are copied).

| path here | upstream path | git object at that commit |
|---|---|---|
| `LICENSE` | `LICENSE` | blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` |
| `lean/lean-toolchain` | `lean/lean-toolchain` | (one line: `leanprover/lean4:v4.34.1`) |
| `lean/ComparatorChallenges/SKFullSupport.lean` | same | blob `2a4bdf1cabdbf723ea9ea2bd1705a6ee038e4f71` |
| `lean/ComparatorChallenges/SKFullSupport.json` | same | blob `1877a6b689adbc033c875b52fadd2d593c3a86ad` |
| `lean/OAI/Probability/SKSupport/` (135 `.lean` files) | same | tree `560a5aaa94414fd30be72170c46ca30a58990c3e` |

To check the copy against upstream:

```sh
git clone --filter=blob:none --no-checkout https://github.com/openai/math.git && cd math
git rev-parse adc7f1241b42e322a6451854ab7e4b4c146bf78a:lean/OAI/Probability/SKSupport   # 560a5aa…
# and in this repository:
git -C <this-repo> rev-parse HEAD:projects/openai-math/lean/OAI/Probability/SKSupport    # the same tree id
```

**Licence.** These files are © OpenAI and licensed under the Apache License, Version 2.0 (the `LICENSE` file
here, copied from the upstream root). The upstream repository has no `NOTICE` file at that commit, and the Lean
files carry no per-file notices. Nothing here was changed. The MIT licence at the root of this explainer
repository does **not** apply to these files.

Authorship, per the upstream README: the repository "contains mathematical manuscripts and supporting proof
artifacts produced by an internal OpenAI model". The manuscript's README names the author as "OpenAI".
