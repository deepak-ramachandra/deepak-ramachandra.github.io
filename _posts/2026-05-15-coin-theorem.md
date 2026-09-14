---
title: "A Story Among My Scratches"
date: 2026-05-15
categories: [Math]
tags: [theorem]
math: true
image:
    path: /assets/img/IMG_5832_sq.jpeg
    alt: Every once in a while, in a period of time that feels long and filled with exhaustion, though very rarely, you might see something like this. Just thinking about it gets your heart racing, and you can feel your confidence coming back. After a long and strenuous climb to the top, it serves as the foothold that you desperately needed. It is not a miracle, maybe it's one out of a hundred, or even one out of a thousand, but it's the one you went to reach and managed to grab. By grabbing and connecting these rare moments, you are able to keep climbing higher and higher.— Fuki Hibarida, (Haikyuu!!)
---

## Preface
My Master's thesis was about proving the [Differential Privacy]({% post_url 2026-05-16-differential-privacy %}) of Thompson Sampling[^agrawal2017] for two arm bandits. Calculating expectations of random variables was well known to me, but the progression of my Master's thesis demanded from me the skill of proving high probability bounds and consequently a deeper understanding of the underlying distribution. While deriving upper bounds for the privacy loss of Thompson Sampling, I was stuck with an expression without a direction to pursue. I needed an intermediate foothold from where I could proceed to the solution intuitively. After making many attempts I finally succeeded in bounding the privacy loss.

Most of the work poured into the main proof involved different approaches and iterations. Among the many rare footholds I managed to grab that contributed to the final submitted work, this result turned out to provide a valid, illustrative, intermediate goal that gave me the confidence for the development of the algebra of my thesis. Looking back through many pages of scratches, the theorem developed in this post also sat close to my heart especially because this is the first high probability bound I ever formulated and worked on. And yet, looking back at my thesis, this result will not be making it into my final draft, since this can be proved using standard Freedman-like inequality[^lee2024]. So, I decided to write this post.

Will point my thesis in due time.

<div style="display:none">
$$\newcommand{\p}{\mathcal{P}}$$
$$\newcommand{\coloneqq}{:=}$$
$$\newcommand{\I}{\mathbb{1}}$$
$$\newcommand{\E}{\mathbb{E}}$$
</div>

## Game
Suppose you are given the liberty to set the bias of a coin to whatever value $b_t \in (0,1)$ before you toss it. If you toss a head, the game is over. However, if you toss a tail, you get a score equal to the bias $b_t$ of the coin you just tossed. The game is played for the total score. Let $X_t=1$ if the toss at time $t$ results in heads and $X_t=0$ if tails. Let $\tau$ be the first time we toss heads. That is, we toss this coin $\tau$ times. Note that the distribution of this random variable $\tau$ depends on how you (the player) set the bias $b_t$ on every turn.

$$\tau = \min\{t \mid X_t=1\}$$

Define $Y$ as the sum of biases until we toss heads for the first time. That is:

$$Y \coloneqq \sum_{t=1}^{\tau-1} b_t$$

So if you choose to be greedy and set the bias of the coin to be $>0.5$, you will most likely toss heads and the game ends right away. On the other hand if you set the bias to be $<0.1$, you will likely toss many tails in a row, and even then the total score might be low. What is a high probability upper bound on the total score earned?



## Theorem
<blockquote class="prompt-info">
<strong>Theorem (Coin).</strong> Suppose we have a coin that changes its bias every time it is tossed. Let $X_t=1$ if the toss at time $t$ results in heads and $X_t=0$ if tails, and let $\mathcal{F}_t = \sigma(X_1, \ldots, X_t)$ be the natural filtration. Define $b_t$ as the conditional probability of heads given the past:
$$b_t \coloneqq \p(X_t=1 \mid \mathcal{F}_{t-1})$$ and assume $b_t \in (0,1)$ almost surely. Then, for any $\delta \in (0, 1)$, as per the above definitions:

$$Y \leq \log(1/\delta) \quad \text{w.p.} \quad 1-\delta$$

</blockquote>


### Original Proof

During the game, we observe $\tau-1$ tails and the last toss will be heads. $\tau$ is the key random variable here. $b_t$ may be a predictable ($\mathcal{F}_{t-1}$ measurable) variable, but we add it to our score only when the past has all tails. If we evaluate it for our concerned path (history containing only tails), we get a known quantity. Define it as $w_t$ instead.

$$w_t := \p(X_t=1|X_1=0,X_2=0,\ldots,X_{t-1}=0)$$

With this, we can define $Y$ as a deterministic function of $\tau$ as $Y = \sum_{t\leq \tau-1}w_t$. The randomness in $Y$ comes solely from the randomness of $\tau$. We define a function

$$
\begin{align*}
    S(T) &:= \sum_{t\leq T}w_t\\
    \text{with that we have,}\quad Y &= S(\tau - 1)
\end{align*}
$$

Here, note that $S$ is also a known function, not just predictable. Also, it is non-negative and strictly increasing. Define another known quantity $T^\star$, such that


$$
\begin{align*}
T^\star := \inf \{t \in \mathbb{N}: S(t) > \log(1/\delta)\}\\
\implies S(T^\star-1) \leq \log(1/\delta) < S(T^\star).
\end{align*}
$$

Now, if the set over which we take the infimum happens to be empty (everything about $S$ is deterministic), then clearly $Y \leq \log(1/\delta)$ with probability 1. Therefore, for the non-trivial case, $T^\star$ is finite. So, with $S$ strictly increasing, we have that $S$ is invertible. Therefore, bounding $Y$ and $\tau$ are essentially the same problem. With $Y = S(\tau - 1)$, we show equality of the following events.

$$\begin{align*}
\{\tau \leq T^\star\} &= \{S(\tau-1) \leq S(T^\star-1)\}\\
&= \{Y \leq \log(1/\delta)\}
\end{align*}
$$

Since $S$ is deterministic, and $w_t \in (0,1)$, we apply $1 - x \leq \exp(-x)$. We use chain rule to write it as a clean product:

$$
\begin{align*}
    \p\left(Y > \log(1/\delta)\right) = \p(\tau > T^\star) &= \p(X_1=0, X_2=0, \ldots,\;X_{T^\star}=0)\\
    &= \prod_{t\leq T^\star}\p(X_t=0| X_1=0, \ldots,\;X_{t-1}=0)\\
    &= \prod_{t\leq T^\star}(1-w_t)\\
    &\leq \exp(-S(T^\star))\\
    &< \exp(-\log(1/\delta)) = \delta.
\end{align*}
$$

<div style="text-align:right">
$\blacksquare$
</div>

> Originally, I had informally proved $\p(Y > u)\leq \exp(-u)$ and arrived at the same conclusion. I was fortunate enough to take Advanced Probability Theory class by [Prof. Ioannis Karatzas](https://www.math.columbia.edu/~ik/) during Fall 2025 to learn the terminology to lay down the proof like so.

---

### Claude's Proof
Define the cumulative sum of biases:

$$S_t \coloneqq \sum_{k=1}^{t}b_k,\quad \text{so,}\;S_0=0.$$

With $0 < b_t < 1$, and $b_t$ predictable, $S_t$ is strictly increasing and predictable.
Define a new sequence:

$$M_0=1,\quad M_t = \I(X_t=0)\exp(b_t)\;M_{t-1}.$$

Starting from $1$, we keep on multiplying $\exp$ of the bias when we toss tails. The moment we toss heads, we set the sequence to zero and we never change it thereafter. Thus $M$ is an absorbing process.

Clearly, $M_t$ is non-negative.
With $\E_t[.] := \E[.|\mathcal{F}_{t-1}]$, we have:

$$
\begin{align*}
\E_t[M_t] &= \E[\I(X_t=0)\exp(b_t)\;M_{t-1}|\mathcal{F}_{t-1}]\\
&= M_{t-1}\exp(b_t)\;\E[\I(X_t=0)|\mathcal{F}_{t-1}]\\
&= M_{t-1}\exp(b_t)\;\p(X_t=0|\mathcal{F}_{t-1})\\
&= M_{t-1}\exp(b_t)\;(1-b_t)\\
&\leq M_{t-1} \qquad \text{since $\exp(-x) \geq 1-x$}
\end{align*}
$$

Hence, $(M_t)_{t \geq 0}$ is a non-negative supermartingale.

Moreover, since $S_t$ is increasing, we get:

$$Y = \sum_{t < \tau} b_t = \sup_{t < \tau}S_t$$

$$\sup_{t \geq 0}M_t = \sup_{t < \tau} \exp(S_t) = \exp(\sup_{t < \tau} S_t) = \exp(Y)$$


Using Ville's inequality:

$$\p\left(\sup_{t \geq 0} M_t \geq a\right)\leq \frac{\E[M_0]}{a}.$$

and also $M_0=1$. This essentially boils down to:

$$\p(\exp(Y) \geq a) \leq \frac{1}{a}$$

Setting $a=1/\delta$, we get the required result.
<div style="text-align:right">
$\blacksquare$
</div>

---

## Conclusion
This post develops the background about an important problem that I came across while working on my thesis. Then, I formulate an equivalent, interprettable and simpler problem and provide an intuitive proof. This result served as a crucial intermediate result that paved the way for swift progress and eventual completion of my Master's thesis. Last, but not the least, I am very grateful for the continual guidance and support of my advisor Prof. Agrawal throughout my Master's thesis.


[^agrawal2017]: Agrawal, S., & Goyal, N. (2017). Near-Optimal Regret Bounds for Thompson Sampling. *Journal of the ACM*, 64(5), Article 30.

[^lee2024]: Lee, H. (2024, June 15). Freedman's and Bernstein's Inequality. *Harin Lee* [Blog]. Retrieved from https://harinboy.github.io/posts/FreedmansInequality/.
