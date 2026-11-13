import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path.cwd()))        # run from the repository root, so `shared` imports
from shared.llm_client import estimate_tokens, get_client  # noqa: E402

plt.style.use("shared/kb.mplstyle")
pd.set_option("display.width", 88)
FIG = "chapters/ch14/figures/"
