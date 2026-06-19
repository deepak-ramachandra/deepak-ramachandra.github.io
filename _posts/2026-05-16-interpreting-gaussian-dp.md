---
title: "Interpreting Gaussian Differential Privacy"
date: 2026-05-16
categories: [Math]
tags: [differential-privacy, statistics, hypothesis-testing]
math: true
image:
    path: /assets/img/gdp_delta_regimes.png
    alt: Plotting δ against the normalized ε/η², the curves stay near 1 in the vacuous regime (ε ≤ η²/4), drop through the transition, and become negligible by ε ≥ η².
---

### Statement
<blockquote class="prompt-tip">
<strong>Main Theorem:</strong>
An $\eta$-GDP mechanism is $(\epsilon, \delta)$-DP for every $\epsilon > 0$, but for $\eta > 4$ a non-trivial $\delta$ is achievable only at $\epsilon = \Theta(\eta^2)$.
</blockquote>

We prove this in two steps. First, we recall the exact conversion from GDP to $(\epsilon, \delta)$-DP, stated here without proof.[^gdp]

<blockquote class="prompt-info">
<strong>Theorem (GDP to $(\epsilon, \delta)$-DP conversion) </strong>
A mechanism is $\eta$-GDP if and only if it is $(\epsilon, \delta(\epsilon))$-DP for all $\epsilon \geq 0$, where

$$
\delta(\epsilon) = \Phi(A) - e^{\epsilon}\, \Phi(B),
\qquad
A := -\frac{\epsilon}{\eta} + \frac{\eta}{2},
\qquad
B := -\frac{\epsilon}{\eta} - \frac{\eta}{2},
$$

and $\Phi$ is the standard Gaussian CDF.
</blockquote>

<style>
    .right{
        text-align:right;
    }
</style>

First, we show that with the tradeoff law $\delta(\epsilon)$, both being small would be too good to be true.

<blockquote class="prompt-info">
<strong>(Monotonicity)</strong>
For a given $\eta$, $\delta(\epsilon)$ is strictly decreasing in $\epsilon$.
</blockquote>

**Proof.** Both $A$ and $B$ satisfy $\frac{dA}{d\epsilon} = \frac{dB}{d\epsilon} = -\frac{1}{\eta}$. Differentiating the conversion,

$$
\frac{d\delta}{d\epsilon}
= \varphi(A)\frac{dA}{d\epsilon} - \left[e^{\epsilon}\Phi(B) + e^{\epsilon}\varphi(B)\frac{dB}{d\epsilon}\right]
= -\frac{\varphi(A)}{\eta} - e^{\epsilon}\Phi(B) + \frac{e^{\epsilon}\varphi(B)}{\eta},
$$

where $\varphi$ is the standard Gaussian pdf. Reusing the identity $\frac{B^2 - A^2}{2} = \epsilon$,

$$
e^{\epsilon}\varphi(B) = \frac{1}{\sqrt{2\pi}}\,e^{\epsilon - B^2/2} = \frac{1}{\sqrt{2\pi}}\,e^{-A^2/2} = \varphi(A),
$$


<div class=right>$\square$</div>
so the two $\frac{1}{\eta}$ terms cancel and $\frac{d\delta}{d\epsilon} = -e^{\epsilon}\,\Phi(B) < 0.$
<br>


---

Note that $\delta$ is strictly decreasing in $\epsilon$ also means that the function is $\delta(\epsilon)$ is invertible as well. We do not need to explicitly find this inverse, we can simply argue its properties indirectly as follows.

>**Lemma (the two regimes)**
>Fix any $\eta > 4$.
>1. <em>Vacuous regime.</em> If $\epsilon \leq \eta^2/4$, then
>\$$
>\delta \geq 1 - \frac{8}{\eta\sqrt{2\pi}}\, e^{-\eta^2/32}.
>$$
>
>1. <em>Negligible regime.</em> If $\epsilon \geq \eta^2$, then
>\$$
>\delta \leq O\\!\left(\eta^{-1}\exp(-\eta^2/8)\right).
>$$
{: .prompt-info}
We use the one-sided tail inequality for the standard Gaussian: for $z \geq 1$,

$$
\frac{e^{-z^2/2}}{2z\sqrt{2\pi}} \leq \Phi(-z) \leq \frac{e^{-z^2/2}}{z\sqrt{2\pi}}.
$$

**Proof.**

*Part (i).* We have

$$
\begin{aligned}
A &= \frac{\eta}{2} - \frac{\epsilon}{\eta} = \frac{\eta}{2} \left(1 - \frac{2\epsilon}{\eta^2}\right) \geq \frac{\eta}{4} \qquad (\text{with } \epsilon \leq \eta^2/4).
\end{aligned}
$$


<div>
With $\eta > 4$, we have $A > 1$. By definition, $|B| \geq |A|$ and $B \leq 0$, so $B < -1$. We also note that $\frac{B^2 - A^2}{2} = \epsilon$, and write
</div>

$$
\begin{aligned}
\delta &= \Phi(A) - e^\epsilon \Phi(B)\\
&= 1 - \Phi(-A) - e^\epsilon \Phi(B)\\
&\geq 1 - \frac{1}{A\sqrt{2\pi}}e^{-A^2/2} - \frac{1}{|B|\sqrt{2\pi}}e^{\epsilon - B^2/2}\\
&\geq 1 - \frac{2}{A\sqrt{2\pi}}e^{-A^2/2}\\
&\geq 1 - \frac{2}{\sqrt{2\pi}}\cdot\frac{4}{\eta}\, e^{-\eta^2/32}\\
&\geq 1 - \frac{8}{\eta\sqrt{2\pi}}\, e^{-\eta^2/32}.
\end{aligned}
$$

*Part (ii).* Here $\Phi$ refers to the left tails. We drop the negative term and apply the upper bound to $\Phi(A)$:

$$
\begin{aligned}
\delta &= \Phi(A) - e^\epsilon\Phi(B) \leq \Phi(A)\\
&\leq \frac{1}{\sqrt{2\pi}\,|A|}\exp(-A^2/2).
\end{aligned}
$$

<div>
If $\epsilon \geq \eta^2$, then $A \leq -\frac{\eta}{2}$ and $B \leq -\frac{3\eta}{2}$; in particular $|A| \geq \frac{\eta}{2} > 2 > 1$, so the tail bound applies and $\delta \leq \frac{2}{\eta\sqrt{2\pi}}\exp(-\eta^2/8) = O\!\left(\eta^{-1}\exp(-\eta^2/8)\right)$.
<div class="right">$\square$</div>
</div>

---
<!-- **Sealing the Main Theorem.** By the monotonicity lemma, $\delta(\epsilon)$ decreases steadily in $\epsilon$. By part (i) it starts vacuous, $\delta \to 1$ for $\epsilon \leq \eta^2/4$, and by part (ii) it is already negligible by $\epsilon \geq \eta^2$. The entire transition from useless to useful is therefore confined to $\epsilon \in [\eta^2/4,\, \eta^2]$ — an interval of both width and location $\Theta(\eta^2)$. -->
Now we have everything we need. $\epsilon \le \eta^2/4$ implies a vacuous $\delta \approx 1$. Moreover, $\epsilon \geq \eta^2$ implies we get an neglible (small $\delta$ is good) value of $\delta$. Since $\delta$ is decreasing in $\epsilon$, this transition from $\delta \approx 1$ to $\delta \approx 0$ happens in the interval $\epsilon \in [\eta^2/4,\, \eta^2]$.
<div class=right>$\blacksquare$</div> Regardless, we can say with certainity that any non-trivial $\delta$ forces $\epsilon = \Theta(\eta^2)$, which proves the Main Theorem.

<hr style="border:1px solid gray">


[^gdp]: Dong, J., Roth, A., and Su, W. J. (2022). Gaussian Differential Privacy. *Journal of the Royal Statistical Society Series B*, 84(1), 3–37. [https://doi.org/10.1111/rssb.12454](https://doi.org/10.1111/rssb.12454)
