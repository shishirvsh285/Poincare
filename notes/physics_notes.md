# Physics notes: the Poincaré Recurrence Theorem

These notes hold the maths behind every slide and every script. Use them to learn the material and to answer questions. The report should be written in the team's own words, so treat this as a study guide, not a draft.

---

## 1. Statement

Let $(\Omega, \mu)$ be a space with a volume (a measure) and let $T : \Omega \to \Omega$ be a map with

1. **finite room**: $\mu(\Omega) < \infty$
2. **no squeezing**: $\mu(T^{-1}A) = \mu(A)$ for every measurable set $A$

Then for every set $A$ with $\mu(A) > 0$, almost every point $x \in A$ has $T^n x \in A$ for infinitely many $n \ge 1$.

"Almost every" means the points that fail form a set of zero volume. A continuous-time flow $\phi_t$ is handled by applying the theorem to the map $T = \phi_{\tau}$ for any fixed $\tau > 0$.

Poincaré stated this in his 1890 memoir on the three-body problem. The clean measure-theory proof below came later (Carathéodory, 1919).

---

## 2. Proof

**Step 1: almost every point returns at least once.**
Let
$$B = \{ x \in A : T^n x \notin A \text{ for all } n \ge 1 \}$$
be the points of $A$ that never come back.

Claim: the sets $B, T^{-1}B, T^{-2}B, \dots$ are pairwise disjoint.
Suppose $x \in T^{-m}B \cap T^{-n}B$ with $m < n$. Put $y = T^m x$. Then $y \in B$ and $T^{n-m} y = T^n x \in B \subset A$. So $y$ returns to $A$ after $n - m$ steps. That contradicts $y \in B$.

Each set has volume $\mu(T^{-k}B) = \mu(B)$ by the no-squeezing rule. They are disjoint and all sit in $\Omega$, so
$$\sum_{k=0}^{K} \mu(B) = (K+1)\,\mu(B) \le \mu(\Omega) \quad \text{for every } K.$$
Since $\mu(\Omega)$ is finite, $\mu(B) = 0$.

**Step 2: almost every point returns infinitely often.**
A point $x \in A$ that returns only finitely often has a last visit to $A$, at some step $m \ge 0$. Then $T^m x \in B$, so $x \in T^{-m}B$. Hence the set of such points sits inside
$$\bigcup_{m \ge 0} T^{-m} B,$$
a countable union of sets of volume $\mu(B) = 0$. Its volume is zero too.

**The picture** (`figures/01_pigeonhole_proof.png`): a disk $U$ is pushed around by an area-preserving shift on a square with wrap-around edges. Every copy has the same area $\pi r^2 \approx 0.0113$, so at most about 88 disjoint copies fit. In practice copy 17 already lands on $U$.

---

## 3. Why Hamiltonian systems satisfy the conditions

**No squeezing (Liouville's theorem).** Hamilton's equations are
$$\dot q_i = \frac{\partial H}{\partial p_i}, \qquad \dot p_i = -\frac{\partial H}{\partial q_i}.$$
The velocity field in phase space has divergence
$$\sum_i \left( \frac{\partial \dot q_i}{\partial q_i} + \frac{\partial \dot p_i}{\partial p_i} \right) = \sum_i \left( \frac{\partial^2 H}{\partial q_i \partial p_i} - \frac{\partial^2 H}{\partial p_i \partial q_i} \right) = 0.$$
A flow with zero divergence keeps every volume fixed. (The rate of change of a volume $V$ carried by the flow is $\dot V = \int_V \nabla \cdot \mathbf{v}\, dV$.)

**Finite room.** Energy is conserved. If the energy surface $\{H = E\}$ (or a thin shell $E \le H \le E + \delta E$) is bounded, the motion lives in a region of finite volume. A gas in a closed box at fixed energy is a good example: positions are bounded by the walls, momenta by the energy.

**Friction breaks it.** Add damping $\dot p = -\partial H / \partial q - \gamma p$. The divergence becomes $-\gamma$, so
$$\dot V = -\gamma V \quad \Rightarrow \quad V(t) = V(0)\, e^{-\gamma t}.$$
Blobs shrink to the stable point and never return.

**What we checked** (`src/02_liouville_blob.py`): a pendulum $H = p^2/2 - \cos q$. A disk of radius 0.45 centred at $(q, p) = (0, 1.55)$ is evolved with `scipy`'s DOP853 integrator (relative tolerance $10^{-10}$). The area is computed from 20,000 boundary points with the shoelace formula.

| case | area at $t = 0$ | area at $t = 12$ | theory at $t = 12$ |
|---|---|---|---|
| no friction | 0.63617 | 0.63616 | 0.63617 |
| $\gamma = 0.25$ | 0.63617 | 0.03167 | 0.03167 |

The tiny drift in the frictionless case comes from the finite number of boundary points as the blob gets very thin.

---

## 4. Example 1: two oscillators with an irrational frequency ratio

$H = \tfrac12(p_1^2 + \omega_1^2 x_1^2) + \tfrac12(p_2^2 + \omega_2^2 x_2^2)$. Each oscillator keeps its own energy, so the state is fixed by two phases $\theta_i = \omega_i t \bmod 2\pi$. The motion is a straight line on a 2-torus.

If $\omega_2/\omega_1$ is irrational, the line never closes and it comes arbitrarily close to every point of the torus (Kronecker / Weyl). In particular it returns arbitrarily close to its start.

**How long until it comes back within $\varepsilon$?** A flux argument gives the mean time between visits to a ball of radius $\varepsilon$ on an $n$-torus with constant velocity $\boldsymbol\omega$:

- Fraction of time spent inside the ball (the flow is uniform on the torus): $f = V_\varepsilon / (2\pi)^n$
- Mean time per visit: mean chord length divided by speed. For straight lines crossing a convex body uniformly, mean chord $= V_\varepsilon / \sigma_\varepsilon$, where $\sigma_\varepsilon$ is the cross-section area seen by the flow ($2\varepsilon$ in 2D, $\pi \varepsilon^2$ in 3D)
- So the mean time between entries is
$$T = \frac{\text{time per visit}}{f} = \frac{(2\pi)^n}{|\boldsymbol\omega|\, \sigma_\varepsilon} \;\propto\; \varepsilon^{-(n-1)}.$$

Each extra oscillator costs another factor of $1/\varepsilon$. Results from `src/03_torus_oscillators.py`:

| $n$ | $\varepsilon$ range | agreement with formula |
|---|---|---|
| 2 | 0.4 to 0.01 | within 1% |
| 3 | 0.5 to 0.08 | within 3% |

---

## 5. Example 2: Arnold's cat map

$$\begin{pmatrix} x \\ y \end{pmatrix} \mapsto \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} \bmod 1 \quad (\text{or } \bmod N \text{ on a pixel grid}).$$

- $\det = 1$, so area is kept (on the grid: it is a one-to-one shuffle of pixels)
- Eigenvalues $\lambda_\pm = (3 \pm \sqrt5)/2 \approx 2.618,\ 0.382$. Lengths along one direction grow by 2.618 each step, so nearby points separate exponentially. That is chaos, with Lyapunov exponent $\ln 2.618 \approx 0.96$
- On an $N \times N$ grid the map is a permutation of $N^2$ pixels. Any permutation of a finite set has finite order, so the picture must return exactly. The return time (period) depends on $N$ in a jumpy way. Dyson and Falk (1992) showed it is never more than $3N$. For $N = 101$ it is 25 (checked in `src/04_cat_map.py`)

Fun fact for questions: on the continuous torus the cat map returns only approximately, like every other example. The exact return is a gift of the finite grid.

---

## 6. Main numerical case: gas in a box and Kac's lemma

**Model.** $N$ non-interacting particles in the unit square, elastic walls, random velocities from a normal distribution. All start in the left half $x < 1/2$.

**Unfolding.** A particle bouncing between $x = 0$ and $x = 1$ with speed $v$ is the same as a point running round a circle of length 2:
$$\theta(t) = \theta_0 + v t \pmod 2, \qquad x = \begin{cases} \theta & \theta < 1 \\ 2 - \theta & \theta \ge 1 \end{cases}$$
So the $x$-state of the gas is a point on an $N$-torus moving in a straight line. Volume is kept and the torus is finite.

**Sampling.** We look once per unit time, $\Delta t = 1$. The look-to-look map is a rotation of the $N$-torus by $(v_1, \dots, v_N)$. For randomly drawn velocities this rotation is ergodic with probability 1 (the numbers $v_i/2$ and 1 are rationally independent).

**Target set.** $A = \{\text{all } x_i < 1/2\}$. On the circle, $x < 1/2$ means $\theta \in [0, 1/2) \cup (3/2, 2)$, which is half the circle. Particles are independent, so $\mu(A) = 2^{-N}$.

**Kac's lemma (1947).** For an ergodic, measure-preserving map on a space of total measure 1, the mean return time to $A$, averaged over starting points in $A$, is
$$\langle T_A \rangle = \frac{1}{\mu(A)}.$$
*Sketch of proof.* Split $A$ into pieces $A_n$ by first return time $n$. The sets $T^k A_n$ for $0 \le k < n$ do not overlap and (by ergodicity) cover the whole space up to zero volume. So $\sum_n n\,\mu(A_n) = 1$. The mean return time is $\sum_n n\,\mu(A_n) / \mu(A) = 1/\mu(A)$.

For the gas this predicts $\langle T \rangle = 2^N$ looks.

**Results** (`src/05_gas_in_box.py`, numbers in `figures/05_results.csv`). About 4000 returns counted for each $N$. The mean gap matches $2^N$ to within about two standard errors for every $N$ from 1 to 14.

| $N$ | measured mean gap | $2^N$ |
|---|---|---|
| 5 | 32.7 ± 0.4 | 32 |
| 10 | 1049 ± 16 | 1024 |
| 14 | 16866 ± 292 | 16384 |

The error bars treat each gap as independent, which is a slight simplification.

**Putting numbers on "eventually".** With one look per millisecond:

| $N$ | wait | compared with the age of the universe ($1.4 \times 10^{10}$ yr) |
|---|---|---|
| 10 | about 1 second | quick |
| 40 | about 35 years | a career |
| 100 | $4 \times 10^{19}$ years | $3 \times 10^{9}$ times longer |
| $10^{27}$ (air in a room) | $2^{10^{27}}$ ms | no words |

---

## 7. Recurrence and the second law

Zermelo (1896) used this theorem to attack Boltzmann. If every state comes back, entropy cannot keep rising. Boltzmann's reply was about time scales. For a macroscopic system the recurrence time is so huge that it never matters in practice. Our Kac plot is that reply in numbers. Recurrence holds in principle. The second law holds for any time we could ever wait.

Two more points that often come up:
- The theorem says nothing about **when**. Kac's lemma fills that gap for ergodic systems
- It needs a **bounded** phase space. An unbounded system, like a gas expanding into empty space forever, need not return at all

---

## 8. Likely questions

- *Is recurrence the same as periodicity?* No. Periodic means exactly the same state again. Recurrence means arbitrarily close. The oscillators with ratio $\varphi$ are recurrent but never periodic.
- *Does chaos prevent recurrence?* No. Chaos changes how soon nearby points separate, not whether volume is kept. The cat map shows this.
- *Do quantum systems recur?* A bounded quantum system with discrete energy levels also shows recurrence (the quantum recurrence theorem of Bocchieri and Loinger, 1957). Not needed for this project, but a nice answer.
- *Why the left half and not "within $\varepsilon$ of the start"?* "All on the left" is a big target, so the waits are measurable. Asking to come back within $\varepsilon$ of the exact start for every particle multiplies the wait by roughly $(1/\varepsilon)^N$, as Example 1 shows.

---

## References

- H. Poincaré, "Sur le problème des trois corps et les équations de la dynamique", *Acta Mathematica* 13 (1890)
- M. Kac, "On the notion of recurrence in discrete stochastic processes", *Bull. Amer. Math. Soc.* 53 (1947)
- V. I. Arnold and A. Avez, *Ergodic Problems of Classical Mechanics* (1968)
- F. J. Dyson and H. Falk, "Period of a discrete cat mapping", *Amer. Math. Monthly* 99 (1992)
- E. Zermelo, *Annalen der Physik* 57 (1896)
