import numpy as np
import matplotlib.pyplot as plt
from math import factorial, log2

n = np.linspace(1, 25, 2000)

y_constant = np.ones_like(n)
y_log = np.log2(n)
y_linear = n
y_nlogn = n * np.log2(n)
y_quadratic = n ** 2
y_cubic = n ** 3
y_exp = 2 ** n
y_factorial = np.array([factorial(int(i)) for i in n])

plt.figure(figsize=(12, 8))

plt.plot(n, y_constant, label=r'$O(1)$ — Constant')
plt.plot(n, y_log, label=r'$O(\log n)$ — Logarithmic')
plt.plot(n, y_linear, label=r'$O(n)$ — Linear')
plt.plot(n, y_nlogn, label=r'$O(n \log n)$ — Linearithmic')
plt.plot(n, y_quadratic, label=r'$O(n^2)$ — Quadratic')
plt.plot(n, y_cubic, label=r'$O(n^3)$ — Cubic')
plt.plot(n, y_exp, label=r'$O(2^n)$ — Exponential')
plt.plot(n, y_factorial, label=r'$O(n!)$ — Factorial')

plt.yscale('log')
plt.xlabel('Input Size (n)', fontsize=13)
plt.ylabel('Operations (log scale)', fontsize=13)
plt.title('Comparison of Common Algorithmic Complexities', fontsize=15)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.savefig('complexity_comparison.png', dpi=150)
plt.show()