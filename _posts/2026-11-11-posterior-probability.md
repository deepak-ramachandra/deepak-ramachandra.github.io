---
title: "Posterior Probability"
date: 2026-11-11
categories: [Math]
tags: [concept]
math: true
image:
    path: /assets/img/post_proba2.png
    alt: In order to know, we must assume.— Prof. Bharath B N, (IIT Dharward)
---
## Information and Probability
I present you a fair coin, that turns up heads or tails fifty-fifty. I toss it and hold it between my palms and sneak a peak for myself. I ask,
>What is the probability that the coin has turned up heads when I open my palms?

Now, I know the outcome that it is indeed tails. However, you don't see the coin. I would answer zero. Either you could say that the question is meaningless since the coin has already turned up as something, it is a matter of knowing the information from the past. Or you could answer based on only what you know - that the coin is fair - and you say half.
>In this sense, under incomplete information, probability can be used to have some opinion about what may happen next.

## Pain of Prejudice
This time, you take the coin from me and toss it two more times and landing on tails. What is the chance it lands on heads the next try? You say: "Half! because the tosses are independent!". Good!

_I may say the coin is fair, but it need not be. Why would you assume I am telling the truth?_ If you saw the same episode of me tossing thrice and getting tails all three times, would you assume the coin is fair? How would you estimate the chance the same coin lands on heads the next try?

>If you don't know the bias of the coin, does your estimate change as you see outcomes of more trials? So far, the coin has been tossed thrice and it has landed only on tails.


<div style="display:none">
$$\newcommand{\p}{\mathcal{P}}$$
$$\newcommand{\coloneqq}{:=}$$
$$\newcommand{\I}{\mathbb{1}}$$
$$\newcommand{\E}{\mathbb{E}}$$
</div>


## Assume so we may know
The coin has some bias $\theta$, however you do not know this. As far you know, you do not have any reason to believe I picked $\theta \geq 0.75$ or $\theta \leq 0.25$. No one value of $\theta$ is more likely than the other from your perspective. Well to be perfectly honest, I would imagine it is hard to make a coin with high bias, but let us not overthink. Regardless, the value has been picked, it is possible that even I know it. _In reality it may not have come from a distribution at all. But then under incomplete information you assume, so you can afford an opinion._

<blockquote class="prompt-tip">
<strong>Assumption:</strong> The bias of the coin $\theta$ is sampled from a uniform distribution.<br>
$$
\theta \sim \text{Uniform}[0,1]
$$
However, $\theta$ is unknown to you. As you see more data, your belief about $\theta$ improves.
</blockquote>

## Formalization
We follow the textbook[^lattimore2020] referenced below, but adapt it to our example for continuity. In our setting, the coin I brought is tossed three times. Your challenge is to figure the bias $\theta$ of the coin.


### Prior probability
Let $(\Theta, \mathcal{G}, Q)$ be a probability space. Here, $\Theta = [0,1]$ the sample space, set of all possible outcomes for the $\theta$ sample. $\mathcal{G} = \mathcal{B}([0, 1])$, the smallest $\sigma$-algebra containing all open intervals in $[0,1]$. ($\mathcal{G}$ is the set of all non-weird subsets of $[0,1]$. There are issues with writing off all subsets.) The function $Q$ represents the probability measure:

$$
Q: \mathcal{G} \rightarrow \mathcal{R}\quad Q(A) \coloneqq \Pr(\theta \in A)
$$

For here, we have, $Q([0,1]) = 1$. $Q(\phi)=0$ and $Q([0.25, 0.7]) = 0.45$. Thus, in this setting, we have assumed a uniform prior $Q$ on the coin's bias $\theta$. Formally, the prior $Q$ is a probability measure on the space $(\Theta, \mathcal{G})$


### Probability Kernel
Let us denote the three outcomes by $X_1, X_2, X_3$. Before we talk about the bias, the list of outcomes of 3 coin tosses remain the same. Namely,

$$
\begin{align*}
S&\coloneqq\text{\{HHH, HHT, HTH, THH, TTH, THT, HTT, TTT\}}.\\
\mathcal{H} &\coloneqq 2^S
\end{align*}
$$

Set of all events $\mathcal{H}$ is just the powerset with $2^8=256$ subsets. So $(S, \mathcal{H})$ is a measurable space.

Now comes the bias $\theta$. If we knew $\theta$, recalling that the tosses are independent as you answered before. This is the conditional probabilty and we use the chain rule below:

$$
P_\theta(\{\text{HHT}\}) = \Pr(X_1=H, X_2=H, X_3=T\,|\theta) = \theta ^2 \times (1-\theta)
$$

If you add many items in the set, you would sum $P_\theta$ over each item.

$$
P_\theta(\{\text{HHT, TTH, HTH}\}) = 2\theta ^2(1-\theta) + (1-\theta)^2\theta.
$$

<blockquote class="prompt-warning">
This seems alright, but does the undergrad formula make sense? Consider the case $\theta=0.5$.

$$
\Pr(X_1=H, X_2=H, X_3=T\,|\theta=0.5) = \frac{\Pr(X_1=H, X_2=H, X_3=T,\theta=0.5)}{\Pr(\theta=0.5)}
$$

For the uniform prior, $P(\theta=0.5) = 0$ and the numerator is a smaller set, so it must be zero too. We are using $\Pr(A\cap B) \leq \Pr(A)$ here. $\Pr_\theta(.) = 0/0$ if we think like this. We will deal with this question a bit further down.
</blockquote>

For a given $\theta$, we have a definitive probability space $(S, \mathcal{H}, P_\theta)$. The possible set of sequences are the same, but the probabilities differ due to $\theta$. This $P = (P_\theta, \,\,\theta \in \Theta)$ is called a model, and also a probability kernel from $(\Theta, \mathcal{G})$ to $(S, \mathcal{H})$.

or any set $B \in \mathcal{G}$, the prior probability can be written in terms of the joint measure: $Q(B) = \mathbb{P}(B \times S)$.


### Joint probability
The prior and the model combine:
* $\Omega = \Theta \times S$ represents the combined sample-space, a point representing $(\theta, X_1, X_2, X_3)$ jointly $\omega = (0.314, HHT)$ is a member of $\Omega$.
* $\mathcal{F} = \mathcal{G} \otimes \mathcal{H}$ represents the joint $\sigma$-algebra. Events involving both $\theta$ and $X_1, X_2, X_3$ are in this set. If $B = [0.25, 0.7]$ then $B \in \mathcal{G}$. And $H = \\{HHT, HHH\\} \in \mathcal{H}$, then this event $(B\times H) \in \mathcal{F}$.
* This joint probability measure $\mathbb{P} = Q \otimes P$ answers questions such as

$$
\Pr(\theta\in [0.25, 0.7], (X_1,X_2,X_3)\in \{HHT, HHH\}) = \mathbb{P}(B\times H) = \text{some value}
$$

* Moreover, for any set $B \in \mathcal{G}$, the prior probability can be written in terms of the joint measure: $Q(B) = \mathbb{P}(B \times S)$.

Now we state an important result from Chapter 3, Kernels, disintegration, and invariance [^kallenberg2021].

<blockquote class="prompt-tip"><strong>Theorem</strong>
Given a probability measure $Q$ on $(\Theta, \mathcal{G})$ and a probability kernel $P$ from $(\Theta, \mathcal{G})$ to $(S, \mathcal{H})$, there is a unique probability measure $\mathbb{P}$ on $(\Omega, \mathcal{F})$, such that:

$$
\mathbb{P}(B \times H) = \int_B P(H)\,Q(d\theta)\quad\text{for all }B \in \mathcal{G},\,H \in \mathcal{H}
$$
</blockquote>

For the uniform prior $Q$, the density is $1$ and thus $Q(d\theta)=d\theta$. The above theorem gives us the license to ride the car we already know to drive, on the streets:

$$
\begin{align*}
    &Pr(\theta\in [0.25, 0.7], (X_1,X_2,X_3)\in \{HHT, HHH\})\\
    &= \int_{0.25}^{0.75}(\theta^2(1-\theta) + \theta^3)d\theta
\end{align*}
$$

[^lattimore2020]: Lattimore, T., & Szepesvári, C. (2020). *Bandit Algorithms*. Cambridge University Press. https://doi.org/10.1017/9781108571401

[^kallenberg2021]: Kallenberg, O. (2021). *Foundations of Modern Probability* (3rd ed.). Springer. https://doi.org/10.1007/978-3-030-61871-1
