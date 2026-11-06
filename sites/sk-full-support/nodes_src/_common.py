"""Helpers shared by the node files (files starting with `_` are not node files).
Each node file keeps its own NODES list:  NODES = []; node = node_adder(NODES)."""
PAPER = ("https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/"
         "Full-support-of-the-zero-temperature-Sherrington-Kirkpatrick-order-parameter-September-27-2026/main.pdf")


def node_adder(NODES):
    def node(id, title, summary, body, quiz, caveats=(), widgets=None):
        NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
    return node


def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


def paper(where, text):
    """A 'Paper wording' paragraph: where in the manuscript, and what it says there (paraphrase or short quote)."""
    return f"\n**In the paper** ([manuscript PDF]({PAPER}), {where}): {text}\n"
