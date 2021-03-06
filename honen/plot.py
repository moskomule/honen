from __future__ import annotations

import os
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt

DISPLAY_AVAILABLE = True
if os.getenv("DISPLAY") is None:
    DISPLAY_AVAILABLE = False
    matplotlib.use("Agg")

from .utils import to_numpy, length_check, in_notebook

__all__ = ["Figure"]

DEFAULT_TICK_PARAM = dict(direction="in",
                          grid_alpha=0.5,
                          grid_linestyle="--")
INITIAL_BAR_DICT = dict(count=0, index=None, width=None)


class Figure(object):
    def __init__(self, boxes: Tuple[int, int] = None, style: str = 'default', figsize: Tuple[int, int] = None,
                 enable_tex_rendering=False):
        matplotlib.style.use(style)
        self.figure = plt.figure(figsize=figsize)
        self._current_ax_position = 0
        self._boxes = (1, 1) if boxes is None else boxes
        self._current_ax: plt.Axes = None
        self._previous_axes = []
        self._bar_dict = INITIAL_BAR_DICT.copy()
        # initialize
        if enable_tex_rendering:
            matplotlib.rcParams['text.usetex'] = True
            matplotlib.rcParams['text.latex.unicode'] = True
        self.next()

    def _refresh(self):
        self._bar_dict = INITIAL_BAR_DICT.copy()

    def next(self) -> Figure:
        self._current_ax_position += 1
        if self._boxes[0] * self._boxes[1] < self._current_ax_position:
            raise UserWarning("No more box!")
        else:
            self._previous_axes.append(self._current_ax)
            self._refresh()
            self._current_ax = self.figure.add_subplot(*self._boxes, self._current_ax_position)
            self.set_tick_params("both", **DEFAULT_TICK_PARAM)
        return self

    def get_current_ax(self):
        return self._current_ax

    def add_plot(self, x, y, *, label=None, linestyle=None, color=None) -> Figure:
        if x is None:
            x = list(range(len(y)))
        length_check(x, y)
        self._current_ax.plot(to_numpy(x), to_numpy(y), label=label, linestyle=linestyle, color=color)
        return self

    def add_fill_plot(self, x, y, *, label=None, color="C0", alpha=0.5) -> Figure:
        if x is None:
            x = list(range(len(y[0])))
        length_check(x, y[0])
        x = to_numpy(x)
        y = to_numpy(y)
        if y.shape[0] == 1:
            raise RuntimeError
        mean = y.mean(axis=0)
        std = y.std(axis=0)
        self._current_ax.plot(x, mean, label=label, color=color)
        self._current_ax.fill_between(x, mean - std, mean + std, facecolor=color, alpha=alpha)
        return self

    def prepare_bar(self, num_groups, width) -> Figure:
        self._bar_dict["index"] = to_numpy(list(range(num_groups)))
        self._bar_dict["width"] = width
        return self

    def add_bar(self, y, *, label=None, alpha=0.6, color=None) -> Figure:
        if self._bar_dict.get("index") is None or self._bar_dict.get("width") is None:
            raise RuntimeError("call prepare_bar(index, width) before calling add_bar")
        index = self._bar_dict["index"]
        width = self._bar_dict["width"]
        count = self._bar_dict["count"]
        length_check(index, y)
        y = to_numpy(y)
        self._current_ax.bar(index + count * width, y, width, alpha=alpha, color=color, label=label)
        self._bar_dict["count"] += 1
        return self

    def add_err_bar(self, y, *, label=None, alpha=0.6, color=None, error_color="0.3") -> Figure:
        y = y.T
        if self._bar_dict.get("index") is None or self._bar_dict.get("width") is None:
            raise RuntimeError("call prepare_bar(index, width) before calling add_bar")
        index = self._bar_dict["index"]
        width = self._bar_dict["width"]
        count = self._bar_dict["count"]
        length_check(index, y[0])
        y = to_numpy(y)
        mean = y.mean(axis=0)
        std = y.std(axis=0)
        self._current_ax.bar(index + count * width, mean, width, yerr=std, alpha=alpha, color=color, label=label,
                             error_kw={'ecolor': error_color})
        self._bar_dict["count"] += 1
        return self

    def add_xlabel(self, text, fontsize=None) -> Figure:
        self._current_ax.set_xlabel(text, fontsize=fontsize)
        return self

    def add_ylabel(self, text, fontsize=None) -> Figure:
        self._current_ax.set_ylabel(text, fontsize=fontsize)
        return self

    def add_box_legend(self, position=None, fontsize=None) -> Figure:
        self._current_ax.legend(loc=position, fontsize=fontsize)
        return self

    def add_global_legend(self, position=None, fontsize=None) -> Figure:
        self.figure.legend(loc=position, fontsize=fontsize)
        return self

    def add_box_title(self, title, fontsize=None) -> Figure:
        self._current_ax.set_title(title, fontsize=fontsize)
        return self

    def add_global_title(self, title, fontsize=None) -> Figure:
        self.figure.suptitle(title, fontsize=fontsize)
        return self

    def add_grid(self) -> Figure:
        self._current_ax.grid()
        return self

    def save(self, name, *, dpi=300) -> Figure:
        self.figure.savefig(name, dpi=dpi)
        return self

    def show(self) -> Figure:
        if in_notebook():
            return self.figure
        elif DISPLAY_AVAILABLE:
            self.figure.show()
        else:
            raise RuntimeWarning("Display unavailable")
        return self

    def set_tick_params(self, axis="both", **kwargs) -> Figure:
        if axis not in ("both", "x", "y"):
            raise RuntimeError
        self._current_ax.tick_params(axis=axis, **kwargs)
        return self

    def set_limits(self, xlims: Tuple[int, int] = None, ylims: Tuple[int, int] = None) -> Figure:
        self._current_ax.set_xlim(xlims)
        self._current_ax.set_ylim(ylims)
        return self

    def tight_layout(self, pad=1.08, h_pad=None, w_pad=None) -> Figure:
        self.figure.tight_layout(pad=pad, h_pad=h_pad, w_pad=w_pad)
        return self

    def set_xticks(self, names, index=None, fontsize=None) -> Figure:
        if index is None:
            index = list(range(len(names)))
        length_check(names, index)
        self._current_ax.set_xticks(index)
        self._current_ax.set_xticklabels(names, fontdict=dict(fontsize=fontsize))
        return self
