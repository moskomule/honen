# honen

`honen` is a matplotlib wrapper. Why `honen`? Google "Honen Tsukioka"

# Usage

```python
from honen import Figure
figure = Figure((2, 1))
figure.add_plot(x=[0,1,2], y=[1, 2, 3]).next().add_plot(x=[0,1,2], y=[2,3,4])
```